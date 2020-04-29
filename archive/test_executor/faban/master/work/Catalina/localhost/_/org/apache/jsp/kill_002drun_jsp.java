package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.engine.RunQ;
import com.sun.faban.harness.security.AccessController;
import java.util.logging.Logger;

public final class kill_002drun_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static java.util.Vector _jspx_dependants;

  public java.util.List getDependants() {
    return _jspx_dependants;
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    JspFactory _jspxFactory = null;
    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      _jspxFactory = JspFactory.getDefaultFactory();
      response.setContentType("text/html");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			"error.jsp", true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\">\n");
      out.write("<!--\n");
      out.write("/* The contents of this file are subject to the terms\n");
      out.write(" * of the Common Development and Distribution License\n");
      out.write(" * (the License). You may not use this file except in\n");
      out.write(" * compliance with the License.\n");
      out.write(" *\n");
      out.write(" * You can obtain a copy of the License at\n");
      out.write(" * http://www.sun.com/cddl/cddl.html or\n");
      out.write(" * install_dir/legal/LICENSE\n");
      out.write(" * See the License for the specific language governing\n");
      out.write(" * permission and limitations under the License.\n");
      out.write(" *\n");
      out.write(" * When distributing Covered Code, include this CDDL\n");
      out.write(" * Header Notice in each file and include the License file\n");
      out.write(" * at install_dir/legal/LICENSE.\n");
      out.write(" * If applicable, add the following below the CDDL Header,\n");
      out.write(" * with the fields enclosed by brackets [] replaced by\n");
      out.write(" * your own identifying information:\n");
      out.write(" * \"Portions Copyrighted [year] [name of copyright owner]\"\n");
      out.write(" *\n");
      out.write(" * $Id$\n");
      out.write(" *\n");
      out.write(" * Copyright 2005-2009 Sun Microsystems Inc. All Rights Reserved\n");
      out.write(" */\n");
      out.write("-->\n");
      out.write("\n");
      com.sun.faban.harness.webclient.UserEnv usrEnv = null;
      synchronized (session) {
        usrEnv = (com.sun.faban.harness.webclient.UserEnv) _jspx_page_context.getAttribute("usrEnv", PageContext.SESSION_SCOPE);
        if (usrEnv == null){
          usrEnv = new com.sun.faban.harness.webclient.UserEnv();
          _jspx_page_context.setAttribute("usrEnv", usrEnv, PageContext.SESSION_SCOPE);
        }
      }
      out.write("\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("  <meta name=\"Author\" content=\"Ramesh Ramachandran\"/>\n");
      out.write("  <meta name=\"Description\" content=\"JSP to setup run.xml for the XForms servlet\"/>\n");
      out.write("  <title>Kill Current Run [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("  <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("  <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("</head>\n");
      out.write("<body>\n");


    String run = RunQ.getHandle().getCurrentRunId();
    if (run == null) {

      out.write("\n");
      out.write("<br><br><b>There is no current run!</b>\n");

    } else {
        String confTimeStr = request.getParameter("confirm");
        long lapse = -1l;
        if (confTimeStr != null) {
            lapse = System.currentTimeMillis() - Long.parseLong(confTimeStr);
        }
        if (lapse < 60000 && lapse > 0) { // The confirm must come within 60 sec

            String runId = request.getParameter("runId");
            String msg;
            if (AccessController.isKillAllowed(usrEnv.getSubject(), runId)) {
                msg = "Run " + runId + " killed!";
                run = RunQ.getHandle().killCurrentRun(runId, usrEnv.getUser());
                if (run == null)
                    msg = "Run " + runId + " no longer active!";
            } else {
                msg = "Permission Denied";
            }

      out.write("\n");
      out.write("<br/>\n");
      out.write("<br/>\n");
      out.write("<b>");
      out.print( msg);
      out.write("</b>\n");
      } else {
            run = RunQ.getHandle().getCurrentRunId();
            if (AccessController.isKillAllowed(usrEnv.getSubject(), run)) {


      out.write("\n");
      out.write("<form name=\"bench\" method=\"post\" action=\"kill-run.jsp\">\n");
      out.write("<input type=\"hidden\" name=\"confirm\" value=\"");
      out.print(System.currentTimeMillis() );
      out.write("\"></input>\n");
      out.write("<input type=\"hidden\" name=\"runId\" value=\"");
      out.print(run );
      out.write("\"></input>\n");
      out.write("\n");
      out.write("<br/><br/><center>Are you sure you want to kill run <b>");
      out.print(run );
      out.write("</b>?<br/>\n");
      out.write("<br/><br/>Please press the \"Kill\" button to continue<br>or choose a different\n");
      out.write("action from the menu on your left.<br/><br/>\n");
      out.write("<input type=\"submit\" value=\"Kill\"></center>\n");
          } else { 
      out.write("\n");
      out.write("<br/><br/><h3><center>Sorry, you have no permission killing run\n");
      out.write("                ");
      out.print( run );
      out.write("</center></h3>                \n");
          }
        }
    }

      out.write("\n");
      out.write("</body>\n");
      out.write("</html>\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          out.clearBuffer();
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
      }
    } finally {
      if (_jspxFactory != null) _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
