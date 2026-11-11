# Automating Canva images and YouTube uploads (proposal, 11 Nov 2026)

What works today, what needs your login, and how to remove that step. Nothing here is built yet.

## Canva: feature images without the browser

**Today.** The Canva connector already works without your browser login: it holds its own OAuth token. It
generated the Cogi image, filed images into folders and moved them. Its one gap: for a generated image it returns
only a 200 px thumbnail. The full 1600 px file needed the logged-in browser, where the preview loads it.

**Option A, stay in Canva (first thing to try).** Make the image part of a design and export the design:

1. `generate-image` → asset ID (as today).
2. Create a 16:9 design that holds that asset (Connect API "create design" with an asset, or `create-design`
   followed by `edit-design` with `insert_fill` on the asset).
3. `export-design` as JPG at 1600 px wide → a download URL → save into the post bundle.

All three steps exist in the connector, so this needs no new setup. I did not try it today; if the connector
refuses, the same flow runs against the Canva Connect API with an integration registered in Canva's developer
portal and a refresh token in `.env`. Field names (asset ID on create, export width) are to be checked on canva.dev.

**Option B, skip Canva for images.** Call an image API (for example Google's Imagen or OpenAI's image API) from a
small script in the `image-generation` skill, with its key in `.env`. Full-size files land straight in the post
folder. You lose the Canva library and its folders.

**Note.** Your Canva subscription has ended (Pro features are off), which may limit AI generation quota and
transparent exports.

## YouTube: uploading Shorts from a script

**How.** YouTube Data API v3, `videos.insert`, with OAuth (scope `youtube.upload`). You consent once in the
browser; the refresh token is stored outside the repo (for example `~/.config/ksopyla-youtube/token.json`). Then
`upload_short.py <mp4> <youtube.md>` reads the title and description from the bundle's `youtube.md`, uploads, prints
the video ID and adds the `youtube-short` embed to the post.

**Catches, in order of importance.**

1. **Uploads stay private until the API project passes an audit.** Google's `videos.insert` reference: videos
   uploaded from unverified API projects created after 28 July 2020 are restricted to private viewing. The fix is
   YouTube's API Services audit (the same form handles quota). Until then, API uploads cannot go public.
2. **Testing-mode tokens expire.** A Google OAuth app left in "Testing" status gets refresh tokens that expire
   after about 7 days (to verify), so the app should be set to "In production" (it can stay unverified for one
   user, with a warning screen at consent).
3. **Quota.** Sources disagree on what an upload costs (1,600 of 10,000 daily units, or a separate upload bucket);
   either way it is enough for a few Shorts a week.
4. **Automatic captions.** Unpublishing YouTube's automatic track (needed because captions are burned in) is a
   Studio step; I don't know of an API call for it.

**Recommendation.** Keep the YouTube upload manual for now (about two minutes) and, if you want it automated,
apply for the audit first: without it the script can only make private videos. For Canva, try Option A on the
next post; it removes the browser step with no new accounts.

The explainer-video skill says the author uploads to his channels himself. Automating the upload changes that
rule, so it stays your decision.
