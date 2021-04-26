public class SA_SELF_COMPARISON {
    /* 43 */
    String test(double d) {
        if (d != d)
            return "\"NaN\"";
        if (d == Double.NEGATIVE_INFINITY)
            return "\"-INF\"";
        if (d == Double.POSITIVE_INFINITY)
            return "\"+INF\"";
        return String.valueOf(d);
    }

    String test01(int d) {
        if (d != d)
            return "\"NaN\"";
        if (d == Double.NEGATIVE_INFINITY)
            return "\"-INF\"";
        if (d == Double.POSITIVE_INFINITY)
            return "\"+INF\"";
        return String.valueOf(d);
    }
}
