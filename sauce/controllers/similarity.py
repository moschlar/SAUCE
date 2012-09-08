# -*- coding: utf-8 -*-
"""Similarity controller module

Only for developing purposes since the final urls are not yet decided

TODO: Map similarity controller beneath assignment controller or similar
TODO: Cleanup interfaces, for now Table + Dendrogram is sufficient
TODO: Cache all_pairs result
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
from repoze.what.predicates import Any, has_permission
from pygmentize import Pygmentize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import Assignment, Submission
from sauce.lib.helpers import udiff
from sauce.lib.auth import has_teacher, has_teachers
from sauce.lib.menu import menu

log = logging.getLogger(__name__)


class SimilarityController(BaseController):

    def __init__(self, assignment):
        self.assignment = assignment
        self.allow_only = Any(has_teacher(self.assignment),
                              has_teacher(self.assignment.sheet),
                              has_teacher(self.assignment.sheet.event),
                              has_teachers(self.assignment.sheet.event),
                              has_permission('manage'),
                              msg=u'You are not allowed to access this page.'
                              )

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.assignment)

#    @expose('sauce.templates.page')
#    def index(self):
#        return dict(heading='Similarity stuff', content=u'''
#<ul>
#  <li><a href="/similarity/similarity">Similarity table</a></li>
#  <li><a href="/similarity/dendrogram">Similarity dendrogram</a></li>
#  <li><a href="/similarity/graph_force">Force-directed graph</a>
#    <ul>
#      <li><a href="/similarity/data_nodes">Plain data (hand-made)</a></li>
#      <li><a href="/similarity/data_nx">Plain data (networkx-made)</a></li>
#    </ul>
#  </li>
#  <li><a href="/similarity/graph_chord">Chord diagram</a>
#    <ul>
#      <li><a href="/similarity/data_matrix">Plain data (hand-made)</a></li>
#    </ul>
#  </li>
#</ul>''')

    def get_similarity(self):
        submissions = sorted(self.assignment.submissions, key=lambda s: s.id, reverse=True)
        matrix = all_pairs([s.source or u'' for s in submissions])
        return matrix

    @expose('sauce.templates.similarity')
    def index(self, cmap_name='RdYlGn', *args, **kw):
        def rgb(v):
            '''Get CSS rgb representation from color map with name'''
            cmap = pylab.get_cmap(cmap_name)
            (r, g, b, _) = cmap(v)
            return 'rgb(' + ','.join('%d' % int(x * 255) for x in (r, g, b)) + ')'
        c.rgb = rgb
        matrix = self.get_similarity()
        return dict(page='assignment', assignment=self.assignment, matrix=matrix,
            submissions=self.assignment.submissions)

    @expose(content_type="image/png")
    def dendrogram(self):
        return dendrogram(self.get_similarity(),
            leaf_label_func=lambda i: str(self.assignment.submissions[i].id),
            leaf_rotation=45)

    #@expose('json')
    def data_matrix(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
        matrix = self.similarity(assignment)['matrix']
        newmatrix = []
        for row in matrix:
            newmatrix.append([int(cell['ratio'] * 10) for cell in matrix[row].itervalues()])
        return dict(matrix=newmatrix)

    #@expose('json')
    def data_list(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
        matrix = self.similarity(assignment)['matrix']
        newlist = []
        for row in matrix:
            newlist.extend(a['ratio'] for a in matrix[row].itervalues())
        return dict(newlist=newlist)

    #@expose('json')
    def data_nodes(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
        s = self.similarity(assignment)
        matrix = s['matrix']
        submissions = s['submissions']
        nodes, links = [], []
        for i, row in enumerate(matrix):
            s = submissions[i]
            nodes.append(dict(name='Submission %d' % s.id, group=s.teams.pop().id if hasattr(s, 'teams') and s.teams else s.user.id))
            for j, cell in enumerate(row):
                if i != j:
                    links.append(dict(source=i, target=j, value=int(cell * 10)))
        return dict(nodes=nodes, links=links)

    #@expose('json')
    def data_nx(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
        matrix = self.similarity(assignment)['matrix']
        import networkx as nx
        from networkx.readwrite import json_graph
        g = nx.Graph()
        for row in matrix:
            g.add_node(row.id, name=unicode(row), group=row.user.id)
            for cell in matrix[row]:
                if cell != row:
                    g.add_edge(row.id, cell.id, value=int(matrix[row][cell]['ratio'] * 10))
        return json_graph.node_link_data(g)
        #return json_graph.adjacency_data(g)

    #@expose('sauce.templates.similarity_graph')
    def graph_matrix(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
        c.backlink = '/similarity/'
        c.style = u'''
.background {
  fill: #eee;
}

line {
  stroke: #fff;
}

text.active {
  fill: red;
}'''

        c.script = u'''
var margin = {top: 80, right: 0, bottom: 10, left: 80},
    width = 720,
    height = 720;

var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),

    c = d3.scale.linear().domain([0,10]).range([d3.rgb(255,0,0), d3.rgb(0,255,0)]).interpolate(d3.interpolateRgb);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("/similarity/data_nodes?assignment='''+unicode(assignment)+'''", function(miserables) {
  var matrix = [],
      nodes = miserables.nodes,
      n = nodes.length;

  // Compute index per node.
  nodes.forEach(function(node, i) {
    node.index = i;
    node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
  });

  // Convert links to matrix; count character occurrences.
  miserables.links.forEach(function(link) {
    matrix[link.source][link.target].z += link.value;
    matrix[link.target][link.source].z += link.value;
    matrix[link.source][link.source].z += link.value;
    matrix[link.target][link.target].z += link.value;
    nodes[link.source].count += link.value;
    nodes[link.target].count += link.value;
  });

  // Precompute the orders.
  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
    count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
    group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  };

  // The default sort order.
  x.domain(orders.count);

  svg.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

  var row = svg.selectAll(".row")
      .data(matrix)
    .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row);

  row.append("line")
      .attr("x2", width);

  row.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return nodes[i].name; });

  var column = svg.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
      .attr("x1", -width);

  column.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return nodes[i].name; });

  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return z(d.z); })
        .style("fill", function(d) { return c(d.z); })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);
  }

  function mouseover(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  d3.select("#order").on("change", function() {
    clearTimeout(timeout);
    order(this.value);
  });

  function order(value) {
    x.domain(orders[value]);

    var t = svg.transition().duration(2500);

    t.selectAll(".row")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .selectAll(".cell")
        .delay(function(d) { return x(d.x) * 4; })
        .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  }

});'''
        return dict(header='Matricks')

    #@expose('sauce.templates.similarity_graph')
    def graph_force(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
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
    /*.charge(-60)
    .linkDistance(60)*/
    .size([width, height]);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/similarity/data_nodes?assignment='''+unicode(assignment)+'''", function(json) {
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

    #@expose('sauce.templates.similarity_graph')
    def graph_chord(self, assignment=1):
        raise Exception('This function is currently broken')  #TODO
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
