import com.fasterxml.jackson.annotation.JsonProperty;

/* https://github.com/future-stardust/url-shrtnr-last/pull/29 */

public class Feedback80 {
    public record ErrorResponse(
            @JsonProperty("reason_code") int reasonCode,
            @JsonProperty("reason_text") String reasonText){

    }
}


