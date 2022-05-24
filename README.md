python3 manage.py load_json --path loss.json

python3 manage.py runserver 0.0.0.0:8000

### Get company_loss data

Note, we have to use POST requests because we are passing a dictionary for complex filter queries.

It is possible to use a GET request but it's better to break the REST protocol here for caching and other benefits

| URL                     | Method |
| ---                     | ---:   |
| `/api/company_loss` | `POST` |

### Schema
#### Request object

| Field Name   | Type       | Default | Description                           
| ---          | ---        | ---:    | ---                                   
| `uuid`   | `string`   |   null  | loss object id for getting one object 
| `nlosses` | `int`      | null       | Number of objects to return 
| `filters`    | `[filter]` | []      | Filters used             
| `sorts` | `[sort]`   | []    | Sorts used                       

`filter` object:

| Field Name | Type     | Default | Description                                                                  |
| ---        | ---      | ---:    | ---                                                                          |
| `name`     | `string` |         | Name of the field to filter                                                  |
| `value`    | `string` |         | Value to filter on                                                           |
| `op`       | `string` | "exact"    | Operation for filter value (can be "exact", "gt", "gte", "lt", or "lte") |

`Sort` object:

| Field Name | Type     | Default | Description                                                                  |
| ---        | ---      | ---:    | ---                                                                          |
| `name`     | `string` |         | Name of the field to filter                                                  |
| `reverse`    | `bool` |  False  | Value to filter on                                                           |

#### Example request body
```
{
	"nlosses": 2,
	"filters": [
		{
			"filter_name": "company_name",
			"value": "Shake Shack Inc"
		},
		{
		"filter_name": "wildfire",
		"value": 0
		},
		{
		"filter_name": "hurricane",
		"value": 0.00017223,
		"op": "gte"
		}
	],
	"sorts": [
		{
			"sort_name": "scenario"
		},
		{
			"sort_name": "total",
			"reverse": true
		}
	]
}
```

#### Response object

List of company loss objects

```
[
    {
        "uuid": "6cbca625-b6fb-4380-9bea-12671fa32014",
        "company_id": "844894bf-f847-4a79-813f-b5226e7bc6e1",
        "company_name": "Shake Shack Inc",
        "scenario": 45,
        "total": 0.00246495237499809,
        "hurricane": 0.00019223,
        "flood": 0.00162271948848887,
        "storm": 0.000650002886509225,
        "wildfire": 0
    }
]
```