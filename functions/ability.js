import getJson from 'get-json'

exports.handler = (event, context, callback) => {
    if (event.httpMethod !== "GET") {
        callback(null, {statusCode: 405, body: event.httpMethod + " not allowed"});
        return;
    }

    let url = "https://pokeapi.netlify.com/api/v2/ability/index.json";

    getJson(url, (error, response) => {
        if (error) {
            console.error(error);
            throw "Request failed: " + url;
        }

        let defaults = {offset: 0, limit: 20};
        let params = event.queryStringParameters;

        params.offset= parseInt(params.offset) || defaults.offset;
        params.limit = parseInt(params.limit) || defaults.limit;

        let resultSlice = response.results.slice(params.offset, params.offset + params.limit);
        let finalResponse = Object.assign(response, {results: resultSlice});

        callback(null, {statusCode: 200, body: JSON.stringify(finalResponse, null, 4)})
    });
};
