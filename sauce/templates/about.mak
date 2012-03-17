<%inherit file="local:templates.master"/>

<%def name="title()">
Learning TurboGears 2.1: Quick guide to the Quickstart pages.
</%def>

${parent.sidebar_top()}
${parent.sidebar_bottom()}
  <div id="getting_started">
    <h2>Architectural basics of a quickstart TG2 site.</h2>
    <p>The TG2 quickstart command produces this basic TG site.  Here's how it works.</p>
    <ol id="getting_started_steps">
      <li class="getting_started">
        <h3>Code my data model</h3>
        <p> When you want a model for storing favorite links or wiki content, 
            the <strong>/model</strong> folder in your site is ready to go.</p>
        <p> You can build a dynamic site without any data model at all. There 
            still be a default data-model template for you if you didn't enable 
            authentication and authorization in quickstart. If you have enabled
            authorization, the auth data-model is ready-made.</p>
      </li>
      <li class="getting_started">
        <h3>Design my URL structure</h3>
        <p> The "<span class="code">root.py</span>" file under the 
            <strong>/controllers</strong> folder has your URLs.  When you 
            called the url or this page (<span class="code"><a href="${tg.url('/about')}">/about</a></span>), 
            the command went through the RootController class to the 
            <span class="code">about</span><span class="code">()</span> method.</p>
        <p> Those Python methods are responsible to create the dictionary of
             variables that will be used in your web views (template).</p>
      </li>
      <li class="getting_started">
        <h3>Reuse the web page elements</h3>
        <p> A web page viewed by user could be constructed by single or 
            several reusable templates under <strong>/templates</strong>. 
            Take 'about' page for example, each reusable template generating 
            a part of the page.</p>

        <p> <strong><span class="code">about.mak</span></strong> - This is the
        template that created this page.  If you take a look at this template
        you will see that there are a lot of wacky symbols, if you are not familiar
        with <a href="http://www.makotemplates.org">Mako</a> you should probably
        check out the docs on their site.  </p>
        
        <p>Let's take a look at what this template does in order of execution.
        The first thing this template does
        is inherit from <strong><span class="code">master.mak</span></strong>. We'll
        go into the details of this later, but for now just know that this
        template is allowed to both call on master.mak, and also override it's
        capabilites.  This inheritance is what gives mako it's power to
        provide reusable templates.
        </p>
        <p>But um, whats that 'local:' stuff about? </p>
        <p>
        Well, TG wants to provide re-usable components like tgext.admin, and also
        provide a way for you to use your default site layouts.  This is done
        easily by providing a shortcut to the namespace of your project, so the
        component template finder can find <strong>your</strong> master.html and format 
        itself the way you want it to.
        </p>
        <p> The next thing about.mak does is to create a function called title()
        which provides the title for the document.  This overrides the title
        method provided by master.mak, and therefore, when the template
        is rendered, it will use the title provided by this funciton.
        
        <p>
        Next, there are a couple of calls to the master template to set up the 
        boxes you see in the page over on the right, We'll examine what
        these are in the master template in a second.  Finally, we get to the meat
        of the document, and that's pretty much all about.mak does
        </p>
        
        <p> <strong><span class="code">master.mak</span></strong> -
        This template provides the overall layout for your project, and
        allows you to override different elements of the overall structure
        of your default look-and-feel.  Let's take a look at this template
        from top to bottom again.</p>
        <p>The first 15 lines provide an overall layout for the document,
        with definitions for the header, title and body.  Each one of these
        sections has been turned into a method that you can change within your
        child templates, but you do not have to provide any single one of them
        TurboGears extensions may however expect these methods to be provided
        to display their content properly.  Keep this in mind if you decide
        to alter your master.mak.  You are of course always free to modify
        your master template, but doing so can render your extensions useless,
        so tread carefully.</p>
        
        <p> The next section describes the overall layout for the body of the
        document, with flash messages appearing at the top, and self.body()
        appearing at the bottom.  self.body will take whatever is not defined
        as a method in your child template and render it in this space.  This
        is really useful because it allows you to be freestyle with your
        body definition.  If you don't want to override any of the master
        template defines, all you have to do is inherit the master, and then
        provide the code you want to appear surrounded by your header and footer.
        </p>
        
        <p>
        Next are the title, header, footer and sidebar defines.  These are all of
        course overriddable.
        </p>
        
        <p>The final define sets up the menubar.  This provides some links,
        as well as a way of highlighing the page you are currently on.
        </p>
      </li>
    </ol>
    <p>Good luck with TurboGears 2!</p>
</div
