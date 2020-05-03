package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.io.FileReader;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.ParamRepository;
import java.io.File;
import com.sun.faban.harness.common.BenchmarkDescription;
import java.io.IOException;
import com.sun.faban.harness.webclient.RunResult;
import com.sun.faban.harness.common.RunId;

public final class resultnavigator_jsp extends org.apache.jasper.runtime.HttpJspBase
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

    String runId = request.getParameter("runId");
    String benchmark = new RunId(runId).getBenchName();

    // First, we try to get the meta info from the results.
    BenchmarkDescription desc = BenchmarkDescription.
            getDescription(benchmark, Config.OUT_DIR + runId);
    if (desc == null)

        // If not, we fetch it from the benchmark meta info.
        desc = BenchmarkDescription.getDescription(benchmark);
    
    String[] status = RunResult.readStatus(runId);
    boolean finished = true;
    if ("STARTED".equals(status[0]))
        finished = false;
    String scale = "";
    if (desc != null) {
        ParamRepository par = new ParamRepository(Config.OUT_DIR + runId +
                File.separator + desc.configFileName, false);
        scale = par.getParameter("fa:scale");
    }

      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <title>Result for Run ");
      out.print(runId);
      out.write(' ');
      out.write('[');
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("        ");
 if (!finished) { 
      out.write("\n");
      out.write("            <meta http-equiv=\"refresh\" content=\"10\">\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <a href=\"/controller/results/get_run_info?runId=");
      out.print( runId );
      out.write("\" target=\"display\">Run&nbsp;Info</a>&nbsp;\n");
      out.write("        ");

           String outputRef = null;
           File summaryFile = new File(Config.OUT_DIR + runId, desc.resultFilePath);
           if (summaryFile.exists()) {
        
      out.write("\n");
      out.write("               <a href=\"output/");
      out.print( runId );
      out.write('/');
      out.print( desc.resultFilePath );
      out.write("\" target=\"display\">Summary&nbsp;Result</a>&nbsp;\n");
      out.write("        ");
 } else { 
      out.write("\n");
      out.write("               <span style=\"color: rgb(102, 102, 102);\">Summary&nbsp;Result</span>&nbsp;\n");
      out.write("        ");

           }
           outputRef = null;
           String[] detailFiles = { "detail.xan", Config.POST_DIR + "detail.xan.html",
                                    "detail.xan.html", "detail.html",
                                    "detail.xml.html" };
           for (int i = 0; i < detailFiles.length; i++) {
               File detailOutput = new File (Config.OUT_DIR + runId, detailFiles[i]);
               if (detailOutput.exists()) {
                   outputRef = "/controller/view/xan_view/" + runId + '/' + detailFiles[i];
                   break;
               }
           }
           if (outputRef == null) {
        
      out.write("\n");
      out.write("                   <span style=\"color: rgb(102, 102, 102);\">Detailed&nbsp;Results</span>&nbsp;\n");
      out.write("        ");
     } else {    
      out.write("\n");
      out.write("                   <a href=\"");
      out.print( outputRef );
      out.write("\" target=\"display\">Detailed&nbsp;Results</a>&nbsp;\n");
      out.write("        ");

               }
           if (desc != null) { 
      out.write("\n");
      out.write("            <a href=\"output/");
      out.print( runId );
      out.write('/');
      out.print( desc.configFileName );
      out.write("\" target=\"display\">\n");
      out.write("                Run&nbsp;Configuration</a>&nbsp;\n");
      out.write("        ");
 } else { 
      out.write("\n");
      out.write("            <span style=\"color: rgb(102, 102, 102);\">Run&nbsp;Configuration</span>&nbsp;\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("        ");
 if (!finished) { 
      out.write("\n");
      out.write("            <a href=\"LogReader?runId=");
      out.print( runId );
      out.write("&startId=end#end\" target=\"display\">Run&nbsp;Log</a>&nbsp;\n");
      out.write("        ");
 } else { 
      out.write("\n");
      out.write("            <a href=\"LogReader?runId=");
      out.print( runId );
      out.write("\" target=\"display\">Run&nbsp;Log</a>&nbsp;\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("            <a href=\"statsnavigator.jsp?runId=");
      out.print( runId );
      out.write("\" target=\"display\">Statistics</a>&nbsp;\n");
      out.write("        <br><br><table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">\n");
      out.write("            <tr>\n");
      out.write("                <td width=\"30%\" style=\"text-align: left; vertical-align: bottom;\">");
      out.print( desc.scaleName );
      out.print( desc.scaleName == null ? "" : ":" );
      out.write(' ');
      out.print( scale );
      out.write(' ');
      out.print( desc.scaleUnit );
      out.write("</td>\n");
      out.write("                <td width=\"40%\" style=\"text-align: center; vertical-align: bottom;\"><b><big>RunID: ");
      out.print( runId );
      out.write("</big></b></td>\n");
      out.write("                <td width=\"30%\" style=\"text-align: right; vertical-align: bottom;\">&nbsp;</td>\n");
      out.write("            </tr>\n");
      out.write("        </table>\n");
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
