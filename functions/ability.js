import getJson from 'get-json'

exports.handler = (event, context, callback) => {
    if (event.httpMethod !== "GET") {
        callback(null, {statusCode: 405, body: event.httpMethod + " not allowed"});
        return;
    }

    let url = "https://pokeapi.netlify.com/api/v2/ability/index.json";

    getJson(url, (error, response) => {
        console.log("error: " + error);
        console.log("response: " + response);

        if (error) {
            throw "Request failed: " + url;
        }

        let defaultParams = {offset: 0, limit: 20};
        console.log("defaults: " + defaultParams);
        let userParams = event.queryStringParameters;
        console.log("user: " + userParams);
        let fullParams = Object.assign(defaultParams, userParams);
        console.log("full: " + fullParams);

        let begin = fullParams.offset;
        let end = fullParams.offset + fullParams.limit;
        console.log("from " + begin + " to " + end);

        let resultSlice = response.results.slice(begin, end);
        console.log("slice: " + resultSlice);
        
        let finalResponse = Object.assign(response, {results: resultSlice});

        callback(null, {statusCode: 200, body: JSON.stringify(finalResponse, null, 4)})
    });
};
