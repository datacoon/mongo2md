# Data stuctures
## Collection naturalmon, Natural monopolies
Registry of natural monopolies maintained by Russian antimonopoly service


| Name        | Type           | Description  |
| ------------- |:-------------:| -----:|
| _id | string | MongoDB Unique identifier
| _uniqkey | string | Unique identifier
| activities | string | Activities name
| activitiesname | string | Activity name
| activitiespart | string | Activity type
| area | string | Area of activity
| decision_date | datetime | Date of decision
| decision_number | string | Number of decision
| numberinreestr | string | Registry number
| orginn | string | INN code of the organization
| orgkpp | string | Organization KPP code
| orglegaladdress | string | Legal address
| orgname | string | Organization name
| regionname | string | Name of the region of Russia

#### Example
```javascript
{
    "_id": {
        "$oid": "5eb1b7bfd47b92cc5e34c620"
    },
    "_uniqkey": "67.1.10",
    "activitiesname": "Раздел I «Услуги по передаче электрической и (или) тепловой энергии»",
    "activitiespart": "Реестр субъектов естественных монополий в топливно-энергетическом комплексе",
    "area": "м-н Пронино",
    "decision_date": {
        "$date": 906681600000
    },
    "decision_number": "39/4",
    "numberinreestr": "67.1.10",
    "orginn": "6729001349",
    "orglegaladdress": "214022, г. Смоленск-22, м-н Пронино",
    "orgname": "ОАО «Смоленский ДОК»",
    "regionname": "Смоленская область"
}
```

