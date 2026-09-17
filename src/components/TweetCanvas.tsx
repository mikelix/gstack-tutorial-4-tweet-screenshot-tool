import { forwardRef } from "react";
import { EmbeddedTweet } from "react-tweet";
import type { Tweet } from "react-tweet/api";
import { backgroundCss, StyleState } from "@/lib/style-state";

export interface TweetCanvasProps {
  tweet: Tweet;
  style: StyleState;
}

/**
 * Renders one tweet with the background/padding/theme wrapper. Owns
 * rendering + visual presentation only — no fetching, no thread awareness,
 * no export logic, no URL state (eng review Section C). ThreadBuilder
 * composes multiple unmodified instances of this component; it never
 * needs to know it's part of a thread.
 */
export const TweetCanvas = forwardRef<HTMLDivElement, TweetCanvasProps>(
  function TweetCanvas({ tweet, style }, ref) {
    return (
      <div
        ref={ref}
        data-theme={style.theme}
        style={{
          display: "inline-block",
          padding: style.padding,
          background: backgroundCss(style.backgroundId),
        }}
      >
        <EmbeddedTweet tweet={tweet} />
      </div>
    );
  },
);
