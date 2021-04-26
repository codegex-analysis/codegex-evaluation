public class RV_EXCEPTION_NOT_THROWN {
    /* 27s */
    void test(){
        try {
            System.out.println();
        }
        catch (Exception e)
        {
            e.printStackTrace();
            new RuntimeException(e);
        }
    }
}
