package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.security.auth.Subject;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.engine.RunQ;
import com.sun.faban.harness.security.AccessController;

public final class pending_002druns_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("<html>\n");
      out.write("    \n");
      out.write("    ");
      com.sun.faban.harness.webclient.UserEnv usrEnv = null;
      synchronized (session) {
        usrEnv = (com.sun.faban.harness.webclient.UserEnv) _jspx_page_context.getAttribute("usrEnv", PageContext.SESSION_SCOPE);
        if (usrEnv == null){
          usrEnv = new com.sun.faban.harness.webclient.UserEnv();
          _jspx_page_context.setAttribute("usrEnv", usrEnv, PageContext.SESSION_SCOPE);
        }
      }
      out.write("\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("        <meta name=\"Author\" content=\"Ramesh Ramachandran\"/>\n");
      out.write("        <meta name=\"Description\" content=\"Pending Runs\"/>\n");
      out.write("        <title>Pending Runs [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <br>\n");
      out.write("        ");

            Subject user = usrEnv.getSubject();
            String[][] pending = RunQ.getHandle().listRunQ();
            if (!(AccessController.isSubmitAllowed(user) || AccessController.isManageAllowed(user))) {
        
      out.write("\n");
      out.write("                <br/>\n");
      out.write("                <br/>\n");
      out.write("                <br/>\n");
      out.write("                <b><center>Permission Denied.</center></b>\n");
      out.write("        ");

            } else if ((pending != null) && (pending.length > 0)) {
                boolean form = false;
                boolean[] killAllowed = new boolean[pending.length];
                for (int i = 0; i < killAllowed.length; i++) {
                    killAllowed[i] = AccessController.isKillAllowed(
                            user, pending[i][1] + '.' + pending[i][0]);
                    if (killAllowed[i])
                        form = true;
                }
                if (form) {
        
      out.write("\n");
      out.write("                <form  method=\"post\" action=\"delete-runs.jsp\">\n");
      out.write("        ");
      } 
      out.write("\n");
      out.write("                    <center>\n");
      out.write("                    <table BORDER=0 CELLPADDING=4 CELLSPACING=3 width=\"80%\" align=\"center\" style=\"padding:2px; border: 2px solid #cccccc;\">\n");
      out.write("                    <tbody>\n");
      out.write("                    <tr>\n");
      out.write("                        <th class=\"header\">Run ID</th>\n");
      out.write("                        <th class=\"header\">Benchmark</th>\n");
      out.write("                        <th class=\"header\">Description</th>\n");
      out.write("                    </tr>\n");
      out.write("        ");

                final String[] rowType = {"even", "odd"};
                for(int i=0; i < pending.length; i++) {
                    String runqDir = pending[i][1] + "." + pending[i][0];

        
      out.write("\n");
      out.write("                    <tr class=\"");
      out.print(rowType[i % 2]);
      out.write("\">\n");
      out.write("                        <td class=\"tablecell\" style=\"text-align: right;\">\n");
      out.write("        ");

                        if (killAllowed[i]) {
        
      out.write("\n");
      out.write("                            <input type=\"checkbox\" name=\"selected-runs\" value=\"");
      out.print(runqDir );
      out.write("\">\n");
      out.write("        ");

                        }
        
      out.write("\n");
      out.write("                            ");
      out.print( pending[i][0] );
      out.write("</td>\n");
      out.write("                        <td class=\"tablecell\">");
      out.print( pending[i][1]);
      out.write("</td>\n");
      out.write("                        <td class=\"tablecell\">");
      out.print( pending[i][2]);
      out.write("</td>\n");
      out.write("                    </tr>\n");
      out.write("         ");
     } 
      out.write("\n");
      out.write("                 </tbody>\n");
      out.write("                 </table>\n");
      out.write("         ");
     if (form) { 
      out.write("\n");
      out.write("                 <br>\n");
      out.write("                 <br>\n");
      out.write("                 <center>\n");
      out.write("                 <input type=\"submit\" value=\"Remove\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("                 <input type=\"reset\"></center>\n");
      out.write("                 </center>\n");
      out.write("                </form>\n");
      out.write("        ");
      }
            } else {
        
      out.write("\n");
      out.write("                <br/>\n");
      out.write("                <br/>\n");
      out.write("                <br/>\n");
      out.write("                <b><center>There are no pending runs.</center></b>\n");
      out.write("        ");
  } 
      out.write("\n");
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
