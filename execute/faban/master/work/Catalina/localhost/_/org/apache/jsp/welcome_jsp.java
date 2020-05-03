package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.common.BenchmarkDescription;

public final class welcome_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("<html>\n");
      out.write("  <head>\n");
      out.write("    <title>Welcome to Faban [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("    <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("    <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("  </head>\n");
      out.write("  <body>\n");
      out.write("  ");
 String bannerName = BenchmarkDescription.getBannerName();
     if (!"Faban".equals(bannerName)) {
         out.println("<br/><br/><br/>");
     }
  
      out.write("\n");
      out.write("  <h2 align=\"center\">Welcome to ");
      out.print(bannerName);
      out.write("</h2>\n");
      out.write("  ");
 // We only show notices if this is not a benchmark integration.
     // The legal notice is not practical if Faban emulates benchmark-specific
     // behavior.
     if ("Faban".equals(bannerName)) {
  
      out.write("\n");
      out.write("        <p><br/><br/></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Copyright &copy; 2006-2009 Sun Microsystems, Inc. All rights reserved.\n");
      out.write("        </font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        U.S. Government Rights - Commercial software. Government users are\n");
      out.write("        subject to the Sun Microsystems, Inc. standard license agreement and\n");
      out.write("        applicable provisions of the FAR and its supplements.</font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Use is subject to license terms.</font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        This distribution may include materials developed by third parties.\n");
      out.write("        </font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Sun, Sun Microsystems, the Sun logo and Java are trademarks or\n");
      out.write("        registered trademarks of Sun Microsystems, Inc. in the U.S. and other\n");
      out.write("        countries.<br/></font></p>\n");
      out.write("        <p><br/></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Copyright &copy; 2006-2009 Sun Microsystems, Inc. Tous droits\n");
      out.write("        r&eacute;serv&eacute;s.</font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        L'utilisation est soumise aux termes du contrat de licence.</font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Cette distribution peut comprendre des composants\n");
      out.write("        d&eacute;velopp&eacute;s par des tierces parties.</font></p>\n");
      out.write("        <p style=\"margin-left: 100px; margin-right: 100px;\"><font size=\"-2\">\n");
      out.write("        Sun, Sun Microsystems, le logo Sun et Java sont des marques de fabrique\n");
      out.write("        ou des marques d&eacute;pos&eacute;es de Sun Microsystems, Inc. aux\n");
      out.write("        Etats-Unis et dans d'autres pays.</font><br/>\n");
      out.write("        </p>\n");
      out.write("  ");

     }
  
      out.write("\n");
      out.write("  </body>\n");
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
