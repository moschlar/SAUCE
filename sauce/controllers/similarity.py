# -*- coding: utf-8 -*-
"""Similarity controller module

Only for developing purposes since the final urls are not yet decided
"""

import math
import logging
from itertools import product
from collections import defaultdict
from difflib import SequenceMatcher
from ripoff import all_pairs, dendrogram
import pylab

# turbogears imports
from tg import expose, abort, flash, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from pygmentize import Pygmentize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import Assignment, Submission
from sauce.lib.helpers import udiff

log = logging.getLogger(__name__)


class SimilarityController(BaseController):

    @expose('sauce.templates.page')
    def index(self):
        return dict(heading='Similarity stuff', content=u'''
<ul>
  <li><a href="/similarity/similarity">Similarity table</a></li>
  <li><a href="/similarity/dendrogram">Similarity dendrogram</a></li>
  <li><a href="/similarity/graph_force">Force-directed graph</a>
    <ul>
      <li><a href="/similarity/data_nodes">Plain data (hand-made)</a></li>
      <li><a href="/similarity/data_nx">Plain data (networkx-made)</a></li>
    </ul>
  </li>
  <li><a href="/similarity/graph_chord">Chord diagram</a>
    <ul>
      <li><a href="/similarity/data_matrix">Plain data (hand-made)</a></li>
    </ul>
  </li>
</ul>''')

    @expose('sauce.templates.similarity')
    def similarity(self, assignment=1, *args, **kw):
        def rgb(v, name='RdYlGn'):
            '''Get CSS rgb representation from color map with name'''
            cmap = pylab.get_cmap(name)
            (r, g, b, _) = cmap(1 - v)
            return 'rgb(' + ','.join('%d' % int(x * 255) for x in (r, g, b)) + ')'
        c.rgb = rgb
        c.backlink = '/similarity/'
        matrix = defaultdict(lambda: defaultdict(dict))
        sm = SequenceMatcher()
        try:
            assignment = Assignment.query.filter_by(id=int(assignment)).one()
        except Exception as e:
            log.debug('Assignment "%s"' % assignment, exc_info=True)
            flash(u'Assignment "%s" does not exist' % assignment, 'error')
            assignment = None
        else:
            if assignment.submissions:
                for (s1, s2) in product(assignment.submissions, repeat=2):
                    if not (matrix[s1][s2] and matrix[s2][s1]):
                        sm.set_seqs(s1.source or u'', s2.source or u'')
                        matrix[s1][s2]['real_quick_ratio'] = matrix[s2][s1]['real_quick_ratio'] = sm.real_quick_ratio()
                        matrix[s1][s2]['quick_ratio'] = matrix[s2][s1]['quick_ratio'] = sm.quick_ratio()
                        matrix[s1][s2]['ratio'] = matrix[s2][s1]['ratio'] = sm.ratio()
            c.image = '/similarity/dendrogram?assignment=%d' % assignment.id
        return dict(page='event', assignment=assignment, matrix=matrix)

    @expose(content_type="image/png")
    def dendrogram(self, assignment=1):
        try:
            assignment = Assignment.query.filter_by(id=int(assignment)).one()
        except Exception as e:
            log.debug('', exc_info=True)
            flash(u'Assignment "%s" does not exist' % assignment, 'error')
            assignment = None
        else:
            return dendrogram(all_pairs([s.source or u'' for s in assignment.submissions]),
                leaf_label_func=lambda i: str(assignment.submissions[i].id),
                leaf_rotation=45)

    @expose('json')
    def data_matrix(self, assignment=1):
        matrix = self.similarity(assignment)['matrix']
        newmatrix = []
        for row in matrix:
            newmatrix.append([int(2**cell['ratio']*100) for cell in matrix[row].itervalues()])
        return dict(matrix=newmatrix)
    @expose('json')
    def data_list(self, assignment=1):
        matrix = self.similarity(assignment)['matrix']
        newlist = []
        for row in matrix:
            newlist.extend(a['ratio'] for a in matrix[row].itervalues())
        return dict(newlist=newlist)

    @expose('json')
    def data_nodes(self, assignment=1):
        matrix = self.similarity(assignment)['matrix']
        nodes, links = [], []
        for i,row in enumerate(matrix):
            nodes.append(dict(name='Submission %d' % row.id, group=row.teams.pop().id if row.teams else row.user.id))
            for j, cell in enumerate(matrix[row]):
                if cell != row:
                    links.append(dict(source=i, target=j, value=int(matrix[row][cell]['ratio'] * 10)))
        return dict(nodes=nodes, links=links)

    @expose('json')
    def data_nx(self, assignment=1):
        matrix = self.similarity(assignment)['matrix']
        import networkx as nx
        from networkx.readwrite import json_graph
        g = nx.Graph()
        for row in matrix:
            g.add_node(row.id, name=unicode(row), group=row.user.id)
            for cell in matrix[row]:
                if cell != row:
                    g.add_edge(row.id, cell.id, weight=matrix[row][cell]['ratio'] * 10)
        return json_graph.node_link_data(g)
        #return json_graph.adjacency_data(g)

    @expose('sauce.templates.similarity_graph')
    def graph_force(self, assignment=1):
        c.backlink = '/similarity/'
        c.style = u'''
circle.node {
  stroke: #fff;
  stroke-width: 1.5px;
}

line.link {
  stroke: #999;
  stroke-opacity: .6;
}'''

        c.script = u'''
var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([width, height]);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/similarity/data_nx?assignment='''+unicode(assignment)+'''", function(json) {
  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll("line.link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.selectAll("circle.node")
      .data(json.nodes)
    .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", function(d) { return color(d.group); })
      .call(force.drag);

  node.append("title")
      .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
});'''
        return dict(header='Force-Directed Layout')

    @expose('sauce.templates.similarity_graph')
    def graph_chord(self, assignment=1):
        c.backlink = '/similarity/'
        c.style = u'''
#chart {
  font: 10px sans-serif;
}

.chord path {
  fill-opacity: .67;
  stroke: #000;
  stroke-width: .5px;
}'''
        c.script = u'''
d3.json("/similarity/data_matrix?assignment='''+unicode(assignment)+'''", function(json) {
  data = json;
    // From http://mkweb.bcgsc.ca/circos/guide/tables/
    var chord = d3.layout.chord()
        .padding(.05)
        .sortSubgroups(d3.descending)
        .matrix(data.matrix);
    
    var width = 600,
        height = 600,
        innerRadius = Math.min(width, height) * .41,
        outerRadius = innerRadius * 1.1;
    
    var fill = d3.scale.category10();
    
    var svg = d3.select("#chart")
      .append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
    svg.append("g")
      .selectAll("path")
        .data(chord.groups)
      .enter().append("path")
        .style("fill", function(d) { return fill(d.index); })
        .style("stroke", function(d) { return fill(d.index); })
        .attr("d", d3.svg.arc().innerRadius(innerRadius).outerRadius(outerRadius))
        .on("mouseover", fade(.1))
        .on("mouseout", fade(1));
    
    var ticks = svg.append("g")
      .selectAll("g")
        .data(chord.groups)
      .enter().append("g")
      .selectAll("g")
        .data(groupTicks)
      .enter().append("g")
        .attr("transform", function(d) {
          return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
              + "translate(" + outerRadius + ",0)";
        });
    
    ticks.append("line")
        .attr("x1", 1)
        .attr("y1", 0)
        .attr("x2", 5)
        .attr("y2", 0)
        .style("stroke", "#000");
    
    ticks.append("text")
        .attr("x", 8)
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) {
          return d.angle > Math.PI ? "end" : null;
        })
        .attr("transform", function(d) {
          return d.angle > Math.PI ? "rotate(180)translate(-16)" : null;
        })
        .text(function(d) { return d.label; });
    
    svg.append("g")
        .attr("class", "chord")
      .selectAll("path")
        .data(chord.chords)
      .enter().append("path")
        .style("fill", function(d) { return fill(d.target.index); })
        .attr("d", d3.svg.chord().radius(innerRadius))
        .style("opacity", 1);
    
    /** Returns an array of tick angles and labels, given a group. */
    function groupTicks(d) {
      var k = (d.endAngle - d.startAngle) / d.value;
      return d3.range(0, d.value, 1000).map(function(v, i) {
        return {
          angle: v * k + d.startAngle,
          label: i % 5 ? null : v / 1000 + "k"
        };
      });
    }
    
    /** Returns an event handler for fading a given chord group. */
    function fade(opacity) {
      return function(g, i) {
        svg.selectAll("g.chord path")
            .filter(function(d) {
              return d.source.index != i && d.target.index != i;
            })
          .transition()
            .style("opacity", opacity);
      };
    }
});'''
        return dict(header='Chord diagram')


    @expose()
    def diff(self, *args, **kw):
        if len(args) != 2:
            abort(404)
        try:
            a = Submission.query.filter_by(id=int(args[0])).one()
            b = Submission.query.filter_by(id=int(args[1])).one()
        except:
            raise
        else:
            pyg = Pygmentize(full=True, linenos=False, title='Submissions %d and %d, Similarity: %.2f' % (a.id, b.id, SequenceMatcher(a=a.source or u'', b=b.source or u'').ratio()))
            return pyg.display(lexer='diff', source=udiff(a.source, b.source, unicode(a), unicode(b)))
