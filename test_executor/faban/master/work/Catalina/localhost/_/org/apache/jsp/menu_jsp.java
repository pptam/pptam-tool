package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.security.auth.Subject;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.security.AccessController;

public final class menu_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      			null, true, 8192, true);
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
      out.write(" * https://faban.dev.java.net/public/CDDLv1.0.html or\n");
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
      out.write('\n');

    boolean submitAllowed = false;
    boolean manageAllowed = false;
    boolean rigAllowed = false;
    if (Config.daemonMode != Config.DaemonModes.DISABLED) {
        Subject user = usrEnv.getSubject();
        submitAllowed = AccessController.isSubmitAllowed(user);
        rigAllowed = AccessController.isRigManageAllowed(user);
        manageAllowed = AccessController.isManageAllowed(user);
    }

      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <title>Faban Menu [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <table BORDER=\"0\" WIDTH=\"100%\" BGCOLOR=\"#FFFFFF\" color=\"#666699\" >\n");
      out.write("            <tr><td VALIGN=\"TOP\"></td></tr>\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/>\n");
 if (submitAllowed) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"selectprofile.jsp\" target=\"main\">Schedule Run</a></td></tr>\n");
 } else { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>Schedule Run</td></tr>\n");
 }
   if (rigAllowed) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"suspend-runs.jsp\" target=\"main\">Suspend Pending Runs</a></td></tr>\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"resume-runs.jsp\" target=\"main\">Resume Pending Runs</a></td></tr>\n");
 } else { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>Suspend Pending Runs</td></tr>\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>Resume Pending Runs</td></tr>\n");
 }
   if (submitAllowed || manageAllowed) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"kill-run.jsp\" target=\"main\">Kill Current Run</a></td></tr>\n");
 } else { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>Kill Current Run</td></tr>\n");
 } 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"/controller/results/list\" target=\"main\">View Results</a></td></tr>\n");
 if (submitAllowed || manageAllowed) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"pending-runs.jsp\" target=\"main\">View Pending Runs</a></td></tr>\n");
 } else { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>View Pending Runs</td></tr>\n");
 }
   if (manageAllowed) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"switchprofile.jsp\" target=\"main\">Switch Profile</a></td></tr>\n");
 } else { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\" style=\"color: rgb(102, 102, 102);\"><br/>Switch Profile</td></tr>\n");
 } 
      out.write('\n');
 if (Config.targetting == true) { 
      out.write("\n");
      out.write("        ");
 if(usrEnv.getUser() != null ) { 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"/controller/results/targetlist?viewAll=true\" target=\"main\">Targets</a></td></tr>\n");
      out.write("        ");
}else{
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"/controller/results/targetlist?viewAll=null\" target=\"main\">Targets</a></td></tr>\n");
      out.write("        ");
}
      out.write('\n');
 } 
      out.write("\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/><a href=\"http://faban.sunsource.net/1.0/docs/toc.html\" target=\"_blank\">Help</a></td></tr>\n");
      out.write("            <tr><td VALIGN=\"CENTER\"><br/></td></tr>\n");
      out.write("            <tr><td VALIGN=\"CENTER\">\n");
      out.write("               <form name=\"tagsearch\" method=\"get\" target=\"main\" action=\"controller/results/list\">\n");
      out.write("                   Tag Search<br>\n");
      out.write("                   <input type=\"text\" name=\"inputtag\" title=\"tag search\" size=\"15\"><br>\n");
      out.write("                   <input type=\"submit\" value=\"Search\">&nbsp;&nbsp;<input type=\"reset\" value=\"Reset\">\n");
      out.write("               </form>\n");
      out.write("            </td></tr>\n");
      out.write("            <tr><td VALIGN=\"TOP\"></td></tr>\n");
      out.write("        </table>\n");
      out.write("    </body>\n");
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
