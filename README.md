[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/fund.html) [![Latest GitHub release](https://img.shields.io/github/v/release/hmlendea/nexusmods-update)](https://github.com/hmlendea/nexusmods-update/releases/latest)

# About

Updates a mod on Nexus Mods.

Takes inspiration from:
 - [greatness7/nexusmods_file_updater](https://github.com/greatness7/nexusmods_file_updater)

# Usage

```yaml

- name: Upload to Nexus
  uses: hmlendea/nexusmods-update@latest
  with:
    account_email_address: ${{secrets.NEXUS_UPLOADER_EMAIL_ADDRESS}} # The email address of the Nexus account
    account_password: ${{secrets.NEXUS_UPLOADER_PASSWORD}} # The password of the Nexus account
    nexus_game_id: "crusaderkings3" # The game's domain name on Nexus
    nexus_mod_id: "11" # The mod's ID on Nexus
    mod_file_name: "more-cultural-names" # The name of the file, as displayed on Nexus
    mod_version: ${{github.ref_name}} # The version of the mod
    file_description: "Changelog: https://github.com/hmlendea/more-cultural-names/releases/${{github.ref_name}}" # File description. Max length: 255
    file_path: "release.zip" # The mod file, which will be uploaded to Nexus
```
