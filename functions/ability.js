import getJson from 'get-json'

exports.handler = (event, context, callback) => {
    if (event.httpMethod !== "GET") {
        callback(null, {statusCode: 405, body: event.httpMethod + " not allowed"});
        return;
    }

    let url = "https://pokeapi.netlify.com/api/v2/ability/index.json";

    getJson(url, (error, response) => {
        console.log("error: %o", error);
        console.log("response: %o", response);

        if (error) {
            throw "Request failed: " + url;
        }

        let defaultParams = {offset: 0, limit: 20};
        console.log("defaults: %o", defaultParams);
        let userParams = event.queryStringParameters;
        console.log("user: %o", userParams);
        let fullParams = Object.assign(defaultParams, userParams);
        console.log("full: %o", fullParams);

        let begin = fullParams.offset;
        let end = fullParams.offset + fullParams.limit;
        console.log("from %o to %o", begin, end);

        let resultSlice = response.results.slice(begin, end);
        console.log("slice: %o", resultSlice);

        let finalResponse = Object.assign(response, {results: resultSlice});

        callback(null, {statusCode: 200, body: JSON.stringify(finalResponse, null, 4)})
    });
};
