import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/* https://github.com/oracle/graal/pull/3288 */

public class Feedback124 {
    private final ConcurrentMap<String, Boolean> registeredLibraries = new ConcurrentHashMap<>();
    void test(String libname){
        if (libname != null && registeredLibraries.putIfAbsent(libname, Boolean.TRUE) != Boolean.TRUE) {
            System.out.println("Hello world.");
        }
    }
}
