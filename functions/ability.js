import getJson from 'get-json'

exports.handler = (event, context, callback) => {
    if (event.httpMethod !== "GET") {
        callback(null, {statusCode: 405, body: event.httpMethod + " not allowed"});
        return;
    }

    let url = "https://pokeapi.netlify.com/api/v2/ability/index.json";

    getJson(url, (error, response) => {
        if (error) {
            throw "Request failed: " + url;
        }

        let defaultParams = {offset: 0, limit: 20};
        let userParams = event.queryStringParameters;
        let fullParams = Object.assign(defaultParams, userParams);

        let begin = fullParams.offset;
        let end = fullParams.offset + fullParams.limit;

        let resultSlice = response.results.slice(begin, end);
        let finalResponse = Object.assign(response, {results: resultSlice});

        callback(null, {statusCode: 200, body: JSON.stringify(finalResponse, null, 4)})
    });
};
