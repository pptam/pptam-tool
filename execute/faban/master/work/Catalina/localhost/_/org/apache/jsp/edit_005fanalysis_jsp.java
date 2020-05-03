package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.webclient.ResultAction;

public final class edit_005fanalysis_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("\n");

    ResultAction.EditAnalysisModel model = (ResultAction.EditAnalysisModel)
             request.getAttribute("editanalysis.model");
 
      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("        <meta name=\"Author\" content=\"Akara Sucharitakul\"/>\n");
      out.write("        <meta name=\"Description\" content=\"Results JSP\"/>\n");
      out.write("        <title>Analyze Runs [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("    <h2><center>");
      out.print( model.head );
      out.write("</center></h2>\n");
      out.write("    <form name=\"analyzename\" method=\"post\" action=\"analyze\">\n");
      out.write("    <table cellpadding=\"0\" cellspacing=\"2\" border=\"0\" align=\"center\">\n");
      out.write("      <tbody>\n");
      out.write("        <tr>\n");
      out.write("          <td style=\"text-align: right;\">Runs: </td>\n");
      out.write("          <td style=\"font-family: sans-serif;\">");
      out.print( model.runList );
      out.write("</td>\n");
      out.write("        </tr>\n");
      out.write("        <tr>\n");
      out.write("          <td style=\"text-align: right;\">Result name: </td>\n");
      out.write("          <td>\n");
      out.write("            <input type=\"text\" name=\"output\"\n");
      out.write("                   title=\"Enter name of the analysis result.\"\n");
      out.write("                   value=\"");
      out.print( model.name );
      out.write("\" size=\"40\">\n");
      out.write("            <input type=\"hidden\" name=\"type\" value=\"");
      out.print( model.type );
      out.write("\"/>\n");
      out.write("          </td>\n");
      out.write("        </tr>\n");
      out.write("      </tbody>\n");
      out.write("    </table><br>\n");
      out.write("    ");

    for (String runId : model.runIds) {
    
      out.write("\n");
      out.write("    <input type=\"hidden\" name=\"select\" value=\"");
      out.print( runId );
      out.write("\"/>\n");
      out.write("    ");

    }
    
      out.write("\n");
      out.write("    <center><input type=\"submit\" name=\"process\" value=\"");
      out.print( model.head );
      out.write("\"\n");
      out.write("            >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"reset\"></center>\n");
      out.write("    </form>\n");
      out.write("    </body>\n");
      out.write("</html>");
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
