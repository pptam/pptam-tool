package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.Map;
import java.util.StringTokenizer;
import com.sun.faban.harness.common.BenchmarkDescription;
import com.sun.faban.harness.security.AccessController;
import com.sun.faban.harness.webclient.UserEnv;
import com.sun.faban.harness.util.FileHelper;
import com.sun.faban.harness.common.Config;
import java.io.File;

public final class new_002drun_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("<head>\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("<meta name=\"Author\" content=\"Ramesh Ramachandran\"/>\n");
      out.write("<meta name=\"Description\" content=\"JSP to setup run.xml for the XForms servlet\"/>\n");
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
      out.write("<title>Please select profile [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");

    String profile = (String)session.getAttribute("faban.profile");
    if (profile == null) {
        profile = request.getParameter("profile");
        session.setAttribute("faban.profile", profile);
    }
    String tags = (String)session.getAttribute("faban.profile.tags");
    if (tags == null) {
        tags = request.getParameter("tags");
        if (profile != null && !"".equals(profile)){
            File profileDir = new File(Config.PROFILES_DIR + profile);
            if(!profileDir.exists())
                profileDir.mkdir();
            File tagsFile = new File(Config.PROFILES_DIR + profile + "/tags");
            if ( (tags != null && !"".equals(tags))) {
                StringBuilder formattedTags = new StringBuilder();
                StringTokenizer t = new StringTokenizer(tags," \n,");
                while (t.hasMoreTokens()) {
                    String nextT = t.nextToken().trim();
                    if( nextT != null && !"".equals(nextT) ){
                        formattedTags.append(nextT + "\n");
                    }
                }
                FileHelper.writeContentToFile(formattedTags.toString(), tagsFile);             
            }
            if(!(tagsFile.length() > 0L))
                    tagsFile.delete();
            if(profileDir.list().length == 0)
                    profileDir.delete();
            session.setAttribute("faban.profile.tags", tags);
        }
    }
    BenchmarkDescription desc = (BenchmarkDescription)
                                        session.getAttribute("faban.benchmark");
    String benchmark = null;
    if (desc == null) {
        Map<String, BenchmarkDescription> bms =
                BenchmarkDescription.getBenchNameMap();
        benchmark = request.getParameter("benchmark");
        desc = bms.get(benchmark);
        session.setAttribute("faban.benchmark", desc);
    }

    if ((profile != null) && (desc != null) && AccessController.
            isSubmitAllowed(usrEnv.getSubject(), desc.shortName)) {

        String templateFile = Config.PROFILES_DIR + profile + File.separator +
                desc.configFileName + "." + desc.shortName;
        File f = new File(templateFile);

        String benchMetaInf = Config.BENCHMARK_DIR + File.separator +
                    desc.shortName + File.separator + "META-INF" +
                    File.separator;

        // String dstFile = Config.TMP_DIR + desc.configFileName;
        if(!f.exists()) // Use the default config file
            templateFile = benchMetaInf + desc.configFileName;

        session.setAttribute("faban.submit.template", templateFile);

        if (desc.configStylesheet != null)
            session.setAttribute("faban.submit.stylesheet", 
                                        benchMetaInf + desc.configStylesheet);

        String url = "bm_submit/" + desc.shortName + '/' + desc.configForm;

      out.write("\n");
      out.write("\n");
      out.write("<meta HTTP-EQUIV=REFRESH CONTENT=\"0;URL=");
      out.print(url);
      out.write("\">\n");
      out.write("<link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("</head>\n");
      out.write("\n");
 }
   else {

      out.write("\n");
      out.write("<body>\n");
      out.write("<form name=\"bench\" method=\"post\" action=\"selectprofile.jsp\">\n");
      out.write("\n");
      out.write("  <br/>\n");
      out.write("  <center><b>Unable to determine profile or benchmark... please select profile</b></center>\n");
      out.write("  <br/>\n");
      out.write("  <center><input type=\"submit\" value=\"OK\"></center>\n");
      out.write("</form>\n");
      out.write("</body>\n");
 } 
      out.write("\n");
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
