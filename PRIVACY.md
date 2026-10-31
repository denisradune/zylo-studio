# zylo uploader — Privacy Policy

_Last updated: 31 October 2026_

**zylo uploader** is a private tool used by the owner of the YouTube channel **zylo** to upload
videos that he produced to his own channel through the YouTube Data API.

## What data the app accesses
- With the owner's consent (Google OAuth), the app requests the `youtube.upload` and
  `youtube.readonly` scopes for the owner's own Google account.
- It uses them only to upload the owner's videos, set their titles, descriptions and thumbnails,
  and read view counts of the channel's own uploads.

## What the app stores
- One OAuth refresh token, kept as a private environment variable in the owner's own environment.
  It is never published, sold or shared.
- The app does not collect, store or process data of any other Google user.

## Sharing
No data is shared with third parties, used for advertising, or used to train AI models.

## Revoking access
Access can be revoked at any time at https://myaccount.google.com/permissions.

## Use of Google user data
zylo uploader's use of information received from Google APIs adheres to the
[Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy),
including the Limited Use requirements, and to the
[YouTube API Services Terms of Service](https://www.youtube.com/t/terms).

## Contact
Questions: open an issue at https://github.com/denisradune/zylo-studio/issues.
