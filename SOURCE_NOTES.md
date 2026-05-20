# Source and filtering notes

This starter library was built by filtering the user's pasted game-word samples, the qigushi 512-word list, and additional family-safe curated terms.

Filtering rules:
- remove adult, political, gambling, weapon, alcohol/tobacco, and brand-heavy entries where possible
- prefer concrete, actable, cute, playful words
- keep category answers unique inside each pack
- include the answer itself in banned_tokens for the app validator
- keep English Gen Z entries family-safe
