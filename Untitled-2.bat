{
    "apps": {
        "http": {
            "servers": {
                "srv0": {
                    "listen": [
                        ":443"
                    ],
                    "routes": [
                        {
                            "handle": [
                                {
                                    "handler": "subroute",
                                    "routes": [
                                        {
                                            "handle": [
                                                {
                                                    "handler": "reverse_proxy",
                                                    "upstreams": [
                                                        {
                                                            "dial": "azure-vote-front:8080"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "match": [
                                {
                                    "host": [
                                        "explore.auditech.xyz"
                                    ]
                                }
                            ],
                            "terminal": true
                        }
                    ]
                }
            }
        }
    }
}