/* https://github.com/cbeust/testng/pull/2497 */

public class Feedback216 {
    private static boolean areNotEqualImpl(Object actual, Object expected) {
        if ((expected == null) && (actual == null)) {
            return false;
        }
        if (expected == null) {
            return actual.equals(actual);
        }
        if (actual == null) {
            return expected.equals(expected);
        }
        return !expected.equals(actual);
    }
}
