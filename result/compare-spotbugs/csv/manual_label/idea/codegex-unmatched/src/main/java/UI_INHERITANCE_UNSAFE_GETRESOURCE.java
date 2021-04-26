import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

public class UI_INHERITANCE_UNSAFE_GETRESOURCE{
    /* 36 */
//    String faviconRef = "/org/eclipse/jetty/favicon.ico";
//    URL fav = this.getClass().getResource(faviconRef);

    /* 18 */
    void test(){
        try (InputStream inStream = this.getClass().getResourceAsStream("/chemcomp.cif.gz")) {
            System.out.println();
        }catch (
                IOException e) {
            System.out.println(e.getMessage());
        }
    }

    /* 48 */
//    void test01(){
//        URL url = this.getClass().getResource("");
//        System.out.println(url.toString());
//    }


}

class subClass extends UI_INHERITANCE_UNSAFE_GETRESOURCE{

}
