import org.eclipse.jetty.server.session.Session;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

public class RC_REF_COMPARISON_BAD_PRACTICE_BOOLEAN {

    void testRC_REF_COMPARISON_BAD_PRACTICE_BOOLEAN(HttpServletRequest request){
        /* 32 */
        HttpSession httpSession = request.getSession(false);
        if (httpSession.getAttribute(Session.SESSION_CREATED_SECURE) != Boolean.TRUE){
            System.out.println();
        }

//        if(getBollean() == Boolean.TRUE){
//            System.out.println();
//        }

        /* 29 */
        Boolean byLocation = Boolean.TRUE;
        if (Boolean.FALSE == byLocation){
            System.out.println();
        }
    }

    Boolean getBollean(){
        return Boolean.FALSE;
    }
}
