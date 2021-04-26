public class EQ_COMPARING_CLASS_NAMES {

    public boolean test(final Object obj) {
        return obj.getClass().getName().equals(obj.getClass().getName()); // no EQ_COMPARING_CLASS_NAMES warningg (potential False positive)
    }

    public boolean compare(final Object obj) {
        return getClass().getName().equals(obj.getClass().getName()); // no EQ_COMPARING_CLASS_NAMES warningg (potential False positive)
    }

    /* From https://github.com/xvik/dropwizard-guicey/blob/33294c39521cf3fa2b0ac502ebbc97eb7f6c15e7/src/main/java/ru/vyarus/dropwizard/guice/module/lifecycle/UniqueGuiceyLifecycleListener.java */
    public boolean equals(final Object obj) {
        return getClass().getName().equals(obj.getClass().getName()); // waning.
    }

}

