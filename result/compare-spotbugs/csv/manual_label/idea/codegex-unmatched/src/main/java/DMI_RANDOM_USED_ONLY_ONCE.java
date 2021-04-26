import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Random;

public class DMI_RANDOM_USED_ONLY_ONCE {

    void testDMI_RANDOM_USED_ONLY_ONCE(){
        /* 34 */
//        String baseDirName = Long.toString(Math.abs(new Random().nextLong()));

        /* 37 */
//        BigInteger serial = BigInteger.valueOf(new SecureRandom().nextLong());

        /* 3 */
//        int rndSeed = new Random().nextInt(10000);
//        /* 47, 48, 59, 60, 61 */
//        String ICIBA = "http://www.iciba.com/";
//        String word = "word";
//        String url = ICIBA + word + "?renovate=" + (new Random(System.currentTimeMillis()).nextInt(899999)+100000);


        /* 49-57 */
        int first = new Random().nextInt(254) + 1;
        System.out.println(first);

        /* 63, 65, 66 */
//        ArrayList<String> words = new ArrayList<>();
//        String word = words.get(new Random(System.nanoTime()).nextInt(words.size()));

//        /* 64,  */
//        String[] attrs = "".split("<br/>");
//        String selectedDefinition = attrs[new Random(System.nanoTime()).nextInt(attrs.length)].trim();
//
//
//        /* 67-85  */
//        int randNumber = new java.util.Random().nextInt(99);

    }

}
