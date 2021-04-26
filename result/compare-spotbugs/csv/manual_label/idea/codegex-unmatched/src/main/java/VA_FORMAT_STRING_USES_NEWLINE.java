public class VA_FORMAT_STRING_USES_NEWLINE {
    void testVA_FORMAT_STRING_USES_NEWLINE(){
        /* 2, 11, 37(jetty.project) */
        String msg = String.format("possible AFP-pairs %d, remain %d after filter 1 remove %d; filter 2 remove %d\n",
                1, 1, 1, 1);

        /* 3-10, 12-14, 16 */
        System.out.println(String.format("maximum score %f, %d\n", 1.0f, 1));

        /* 17 */
        // SpotBugs fn
        String nThreads = "hello world";
        System.out.printf(nThreads +" threads, time: %4.1fs -- x%2.1f\n",1.0f, 1.0f);

        /* 38-42 */
        StringBuilder supported = new StringBuilder();
        supported.append(String.format("%" + 10 + "s: %s %s\n", "hello", "world", ""));
        supported.append(String.format("    %11s = %s %s\n", "hello", "world", "!"));
    }
}
