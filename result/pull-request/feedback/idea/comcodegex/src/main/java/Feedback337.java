/* https://github.com/jenkinsci/workflow-cps-plugin/pull/422 */

public class Feedback337 {
    static class WithStartFailureStepExecution extends AbstractStepExecutionImpl {

        WithStartFailureStepExecution(final StepContext context) {
            super(context);
        }
    }

}


class AbstractStepExecutionImpl{
    public AbstractStepExecutionImpl(StepContext context){

    }
}

class StepContext{

}