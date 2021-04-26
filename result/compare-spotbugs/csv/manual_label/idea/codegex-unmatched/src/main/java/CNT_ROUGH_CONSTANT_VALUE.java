

public class CNT_ROUGH_CONSTANT_VALUE {
    /* 15 */
    void test(){
        double sigma1 = 0.01;
        double result = Math.sqrt(6.28) * sigma1;
        System.out.println(result);
    }

    void test01(){
        double sigma1 = 3.14;
        double result = Math.sqrt(sigma1) * sigma1;
        System.out.println(result);
    }

    void test02(){
        double sigma1 = 0.01;
        double result = Math.sqrt(3.14) * sigma1;
        System.out.println(result);
    }

    void test03(){
        double sigma1 = 6.2831;
        double result = Math.sqrt(sigma1);
        System.out.println(result);
    }
}
