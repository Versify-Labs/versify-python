exports = function (changeEvent) {
    /*
      Accessing application's values:
      var x = context.values.get("value_name");
  
      Accessing a mongodb service:
      var collection = context.services.get("mongodb-atlas").db("dbname").collection("coll_name");
      collection.findOne({ owner_id: context.user.id }).then((doc) => {
        // do something with doc
      });
  
      To call other named functions:
      var result = context.functions.execute("function_name", arg1, arg2);
  
      Try running in the console below.
    */
    const AWS = require('aws-sdk');

    const operationType = changeEvent.operationType;

    // Determine which document to use based on the operation type
    let document = {}
    if (changeEvent.fullDocument) {
        document = changeEvent.fullDocument;
    } else if (changeEvent.fullDocumentBeforeChange) {
        document = changeEvent.fullDocumentBeforeChange;
    } else {
        document = changeEvent.documentKey;
    }
    const objectType = document.object;

    // Parse changeEvent for detail_type and detail
    let detail = {};
    let detailType = "";
    switch (operationType) {
        case 'insert':
            detail = document;
            detailType = `${objectType}.created`;
            break;
        case 'update':
            detail = document;
            detailType = `${objectType}.updated`;
            break;
        case 'replace':
            detail = document;
            detailType = `${objectType}.updated`;
            break;
        case 'delete':
            detail = document;
            detailType = `${objectType}.deleted`;
            break;
        default:
            detail = document;
            detailType = `${objectType}.modified`;
            break;
    }

    // Publish event to EventBridge bus
    const config = {
        apiVersion: '2015-10-07',
        region: 'us-east-1',
        accessKeyId: context.values.get("AWS_ACCESS_KEY_ID"),
        secretAccessKey: context.values.get("AWS_SECRET_ACCESS_KEY")
    };

    // const eventBridge = new AWS.EventBridge(config);
    const eventClient = new AWS.CloudWatchEvents(config);
    const params = {
        Entries: [
            {
                EventBusName: "versify",
                Source: "versify",
                DetailType: detailType,
                Detail: JSON.stringify(detail)
            }
        ]
    };

    eventClient.putEvents(params, function (err, data) {
        if (err) console.log(err, err.stack);
        else console.log(data);
    });


    return { arg: changeEvent };
};