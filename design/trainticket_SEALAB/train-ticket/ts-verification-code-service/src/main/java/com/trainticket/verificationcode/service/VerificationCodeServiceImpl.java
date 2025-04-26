package com.trainticket.verificationcode.service;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

import com.trainticket.verificationcode.domain.VerificationCodeValue;
import com.trainticket.verificationcode.repository.VerificationCodeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import com.trainticket.verificationcode.util.CookieUtil;
@Service
public class VerificationCodeServiceImpl implements VerificationCodeService{

    //private Map<String, String> map = new HashMap<String, String>();
    @Autowired
    public VerificationCodeRepository verificationCodeRepository;

    private static char mapTable[] = {
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
            'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };


    public static final String CAPTCHA = "captcha:";

    public static final String CAPTCHA_CODE = "code";

    public static final String CAPTCHA_CHECKED = "checked";

    public static final int CAPTCHA_EXPIRED = 1000;

    @Override
    public Map<String, Object> getImageCode(int width, int height, OutputStream os, HttpServletRequest request, HttpServletResponse response, HttpHeaders headers) {
        Map<String,Object> returnMap = new HashMap<String, Object>();
        if (width <= 0) width = 60;
        if (height <= 0) height = 20;
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        
        Graphics g = image.getGraphics();
        
        Random random = new Random();
        
        g.setColor(getRandColor(200, 250));
        g.fillRect(0, 0, width, height);
        
        g.setFont(new Font("Times New Roman", Font.PLAIN, 18));
        
        g.setColor(getRandColor(160, 200));
        for (int i = 0; i < 168; i++) {
            int x = random.nextInt(width);
            int y = random.nextInt(height);
            int xl = random.nextInt(12);
            int yl = random.nextInt(12);
            g.drawLine(x, y, x + xl, y + yl);
        }
        
        String strEnsure = "";
        
        for (int i = 0; i < 4; ++i) {
            strEnsure += mapTable[(int) (mapTable.length * Math.random())];
            
            g.setColor(new Color(20 + random.nextInt(110), 20 + random.nextInt(110), 20 + random.nextInt(110)));
            
            String str = strEnsure.substring(i, i + 1);
            g.drawString(str, 13 * i + 6, 16);
        }
        
        g.dispose();
        returnMap.put("image",image);
        returnMap.put("strEnsure",strEnsure);

        Cookie cookie = CookieUtil.getCookieByName(request,"YsbCaptcha");
        String cookieId;
        if(cookie == null){
            cookieId = UUID.randomUUID().toString().replace("-", "").toUpperCase();
            CookieUtil.addCookie(response, "YsbCaptcha", cookieId, CAPTCHA_EXPIRED);
        }else{
            if(cookie.getValue() != null){
                cookieId = UUID.randomUUID().toString().replace("-", "").toUpperCase();
                CookieUtil.addCookie(response, "YsbCaptcha", cookieId, CAPTCHA_EXPIRED);
            }else {
                cookieId = cookie.getValue();
            }
        }

        verificationCodeRepository.save(new VerificationCodeValue(cookieId,strEnsure));
        //map.put(cookieId,strEnsure);

        return returnMap;
    }

    @Override
    public boolean verifyCode(HttpServletRequest request, HttpServletResponse response, String receivedCode, HttpHeaders headers){
        boolean result = false;
        Cookie cookie = CookieUtil.getCookieByName(request,"YsbCaptcha");
        String cookieId;
        if(cookie == null){
            cookieId = UUID.randomUUID().toString().replace("-", "").toUpperCase();
            CookieUtil.addCookie(response, "YsbCaptcha", cookieId, CAPTCHA_EXPIRED);
        }else{
            cookieId = cookie.getValue();
        }

        VerificationCodeValue value = verificationCodeRepository.findByCookie(cookieId);
        if(value == null){
            return false;
        }

        String code = value.getVerificationCode();
        //String code = map.get(cookieId);

        if(code.equals(receivedCode.toUpperCase())){
            result = true;
        }
        return result;
    }

    static Color getRandColor(int fc, int bc) {
        Random random = new Random();
        if (fc > 255) fc = 255;
        if (bc > 255) bc = 255;
        int r = fc + random.nextInt(bc - fc);
        int g = fc + random.nextInt(bc - fc);
        int b = fc + random.nextInt(bc - fc);
        return new Color(r, g, b);
    }
}


