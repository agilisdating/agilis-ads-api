# Security

## Reporting a problem

If you find a security problem in the Agilis Advertising API, the Ad Portal or this repository, please email **help@agilis.dating** with "Security" in the subject. Include what you found, how to reproduce it, and how we can contact you.

Please don't open a public issue, and don't access, change or delete data that isn't yours while testing. Use your own Test-mode key.

We'll acknowledge your report and keep you updated while we fix it.

## If your API key is exposed

If a key has been committed to a repository, pasted in a public place or shared by mistake:

1. Sign in to the Ad Portal, open **Manage API Keys** in the same mode (Test or Live) and select **Roll key**. The old key stops working at once.
2. Update your systems with the new key.
3. Tell us at help@agilis.dating if you think it was a Live key that was used by someone else.

Keep keys in environment variables or a secrets manager, never in code. This repository's `.gitignore` excludes `.env` files.
