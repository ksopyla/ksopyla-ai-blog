function css(name) {
  return "rgb(" + getComputedStyle(document.documentElement).getPropertyValue(name) + ")";
}

let isDark = document.documentElement.classList.contains("dark");

mermaid.initialize({
  theme: "base",
  themeVariables: {
    background: css("--color-neutral"),

    primaryColor: isDark ? css("--color-primary-700") : css("--color-primary-200"),
    primaryTextColor: isDark ? css("--color-neutral-200") : css("--color-neutral-700"),
    primaryBorderColor: isDark ? css("--color-primary-500") : css("--color-primary-400"),

    secondaryColor: isDark ? css("--color-secondary-700") : css("--color-secondary-200"),
    secondaryTextColor: isDark ? css("--color-neutral-200") : css("--color-neutral-700"),
    secondaryBorderColor: css("--color-secondary-400"),

    tertiaryColor: isDark ? css("--color-neutral-700") : css("--color-neutral-100"),
    tertiaryTextColor: isDark ? css("--color-neutral-200") : css("--color-neutral-700"),
    tertiaryBorderColor: isDark ? css("--color-neutral-300") : css("--color-neutral-400"),

    nodeTextColor: isDark ? css("--color-neutral-200") : css("--color-neutral-700"),
    clusterBkg: isDark ? css("--color-primary-950") : css("--color-primary-50"),
    clusterBorder: isDark ? css("--color-primary-500") : css("--color-primary-400"),
    titleColor: isDark ? css("--color-neutral-200") : css("--color-neutral-700"),
    edgeLabelBackground: isDark ? css("--color-neutral-800") : css("--color-neutral-100"),
    lineColor: isDark ? css("--color-neutral-300") : css("--color-neutral-600"),

    fontFamily:
      "ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,segoe ui,Roboto,helvetica neue,Arial,noto sans,sans-serif",
    fontSize: "16px",

    pieTitleTextSize: "19px",
    pieSectionTextSize: "16px",
    pieLegendTextSize: "16px",
    pieStrokeWidth: "1px",
    pieOuterStrokeWidth: "0.5px",
    pieStrokeColor: isDark ? css("--color-neutral-300") : css("--color-neutral-400"),
    pieOpacity: "1",
  },
});
