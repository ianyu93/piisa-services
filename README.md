# piisa-services
This is a collection of services that can be used to extract PII from text via [PIISA](https://piisa.org/) framework.

## Deployed Services
See API documentation for each service:
- [PIISA Presidio](https://piisa-presidio-service-jvmkj3qila-uc.a.run.app/docs)

Example to annotate by default, but redact email addresses and replace names with synthetic names:
```
curl -X 'POST' \
  'https://piisa-presidio-service-jvmkj3qila-uc.a.run.app/pii-process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "\nAnjali Mehra was born on July 15, 1987 in the bustling city of New York. She is an accomplished author \nand journalist who has written several best-selling novels and contributed to numerous publications. \nAnjali grew up in a small apartment in Manhattan with her parents, both of whom were immigrants from India. \nFrom a young age, she showed a keen interest in writing and storytelling, often regaling her family and \nfriends with tales of adventure and intrigue. After graduating from Columbia University with a degree in \nEnglish literature, Anjali began her career as a freelance writer for various magazines and websites. \nHer work quickly gained recognition, and she soon landed a job at one of the most prestigious publishing \nhouses in the country. Over the years, Anjali has published several successful novels that have captivated\nreaders around the world. Her latest book, \"The Secret Garden,\" was released earlier this year and has\nalready become a global sensation. In addition to her writing, Anjali is also known for her activism and\nphilanthropy. She frequently speaks out against social justice issues and works tirelessly to raise awareness\nand funds for various causes. Despite her busy schedule, Anjali always makes time for her loved ones. She is \nmarried to fellow author, David Chen, and they have two children together. When she'\''s not working or volunteering, \nAnjali can be found spending quality time with her family or exploring new places and cultures. If you want to \nget in touch with Anjali, you can reach her at her fake phone number (212) 555-1234 or her made-up \naddress: 123 Main Street, New York, NY 10001.\n",
  "lang": "en",
  "entities": [
    "AGE",
    "BANK_ACCOUNT",
    "BLOCKCHAIN_ADDRESS",
    "CREDIT_CARD",
    "DATE",
    "EMAIL_ADDRESS",
    "GOV_ID",
    "IP_ADDRESS",
    "KEY",
    "LICENSE_PLATE",
    "LOCATION",
    "MEDICAL",
    "NORP",
    "ORG",
    "OTHER",
    "PASSWORD",
    "PERSON",
    "PHONE_NUMBER",
    "USERNAME"
  ],
  "default_policy": "annotate",
  "config": {"pii-transform:main:v1": {"policy": {"PERSON": "synthetic", "EMAIL_ADDRESS": "redact"}}}
}'
```

```
{"output":"\nAmy Gonzalez was born on July 15, 1987 in the bustling city of <LOCATION:New York>. She is an <GOV_ID:accomplished> author \nand journalist who has written several best-selling novels and contributed to numerous <GOV_ID:publications>. \nAnjali grew up in a small apartment in <LOCATION:Manhattan> with her parents, both of whom were immigrants from <LOCATION:India>. \nFrom a young age, she showed a keen interest in writing and <GOV_ID:storytelling>, often regaling her family and \nfriends with tales of adventure and intrigue. After graduating from Columbia University with a degree in \nEnglish literature, Faith Taylor began her career as a freelance writer for various magazines and websites. \nHer work quickly gained recognition, and she soon landed a job at one of the most prestigious publishing \nhouses in the country. Over the years, Anjali has published several successful novels that have captivated\nreaders around the world. Her latest book, \"The Secret Garden,\" was released earlier this year and has\nalready become a global sensation. In addition to her writing, Anjali is also known for her activism and\n<GOV_ID:philanthropy>. She frequently speaks out against social justice issues and works tirelessly to raise awareness\nand funds for various causes. Despite her busy schedule, Anjali always makes time for her loved ones. She is \nmarried to fellow author, Lisa Robinson, and they have two children together. When she's not working or <GOV_ID:volunteering>, \nAnjali can be found spending quality time with her family or exploring new places and cultures. If you want to \nget in touch with Anjali, you can reach her at her fake phone number <PHONE_NUMBER:(212) 555-1234> or her made-up \naddress: 123 Main Street, <LOCATION:New York>, <LOCATION:NY 10001>.\n"}
```