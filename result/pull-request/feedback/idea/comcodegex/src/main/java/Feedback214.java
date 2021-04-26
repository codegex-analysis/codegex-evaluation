/* https://github.com/cgeo/cgeo/pull/10085 */

public class Feedback214 {
    void test(String additionalInfo){
        String str = String.format(additionalInfo.isBlank() ? additionalInfo + "\n\n" : "a");
        str = String.format("\n\n");
        System.out.printf("\n\n", additionalInfo);
        System.out.printf("%s\n\n", additionalInfo);
        System.out.printf(additionalInfo + "\n\n");
        System.out.printf("\n\n" + additionalInfo);
    }
}
