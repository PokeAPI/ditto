import getJson from 'get-json'

const baseUrl = "https://pokeapi.netlify.com/api/v2";

function targetUrlForPath(path) {
    let target = baseUrl;
    target += path;
    if (!target.endsWith("/")) {
        target += "/";
    }
    target += "index.json";
    return target;
}

function extractParams(query) {
    let defaults = {offset: 0, limit: 20};
    return {
        offset: parseInt(query.offset) || 0,
        limit: parseInt(query.limit) || 20,
    }
}

function getPageUrl(path, params) {
    if (params == null) {
        return null;
    }
    return baseUrl + path + "?offset=" + params.offset + "&limit=" + params.limit;
}

function getPreviousPage(params) {
    let newPage = {
        begin: params.offset - params.limit,
        end: params.offset,
    }

    if (newPage.begin < 0) {
        newPage.begin = 0;
    }

    // it's a prev page only if we've moved back
    if (newPage.begin < params.offset) {
        return {
            offset: newPage.begin,
            limit: newPage.end - newPage.begin,
        };
    }

    return null;
}

function getNextPage(params, count) {
    let newPage = {
        begin: params.offset + params.limit,
        end: params.offset + params.limit * 2,
    }

    if (newPage.end > count) {
        newPage.end = count;
    }

    // it's a next page only if we've moved forward
    if (newPage.end > params.offset + params.limit) {
        return {
            offset: newPage.begin,
            limit: newPage.end - newPage.begin,
        }
    }

    return null;
}

exports.handler = (event, context, callback) => {
    if (event.httpMethod !== "GET") {
        callback(null, {statusCode: 405, body: event.httpMethod + " not allowed"});
        return;
    }

    console.log(event);
    
    let url = targetUrlForPath(event.path);

    getJson(url, (error, response) => {
        if (error) {
            console.error(error);
            throw "Request failed: " + url;
        }

        let params = extractParams(event.queryStringParameters);
        let resultSlice = response.results.slice(params.offset, params.offset + params.limit);
        let finalResponse = Object.assign(response, {
            next: getPageUrl(event.path, getNextPage(params, response.count)),
            previous: getPageUrl(event.path, getPreviousPage(params)),
            results: resultSlice,
        });

        callback(null, {statusCode: 200, body: JSON.stringify(finalResponse, null, 4)})
    });
};
