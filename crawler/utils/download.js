/*
 * Created on Oct 16, 2013
 *
 * author: qwang
 *
 * This script is for downloading dynamic web page, and run javascript inside
 * page with phantomjs.
 *
 * Usage:
 * phantomjs download.js URL [--user-agent=USER-AGENT] [--referer=REFERER] [--timeout=TIMEOUT]
 *
 * Output:
 * if succeed, html of the requested page after javascript executed.
 * if failed, error header(###RequestError###) at the beginning, and then error description.
 */

function exit(){
    phantom.exit();
}
// error header, if response starts with this header, error happened.
var error_header = "###RequestError###";

// get args from system module
var args = require("system").args;

var url = null;
var root_domain = null;
var user_agent = null;
var referer = null;
// deefault time out, 60 seconds
var timeout = 60000;
var top_domains = ['com', 'edu', 'gov', 'int', 'mil', 'net', 'org', 'biz', 'info', 'pro', 'name', 'museum',
        'coop', 'aero', 'idv', 'xxx'];

var _white_list = {
    '163.com': ['netease.com'],
    'cntv.cn': ['cctv.com', 'cctvpic.com'],
    'qq.com': ['gtimg.cn', 'gtimg.com'],
};

function get_domain(url){
    var r = /:\/\/(.[^\/]+)/;
    return url.match(r)[1];
}
function get_root_domain(url){
    var domain = get_domain(url);
    var frags = domain.split('.');
    var start = false;
    var root = null;
    for (var i=frags.length-1; i >= 0; i--){
        if (i == frags.length - 1){
            continue;
        } else if (i == (frags.length - 2) && top_domains.indexOf(frags[i]) == -1){
            root = frags.slice(i).join(".");
            break;
        } else if (i == (frags.length - 3)){
            root = frags.slice(i).join(".");
            break;
        }
    }
    if (root == null){
        return domain;
    }
    return root;
}

// timeout callback
function onResourceTimeout(){
    console.log(error_header);
    console.log('Request Timeout');
};
// resource error callback
function onResourceError(resourceError) {
    // only log error for main frame
    if (resourceError.url == url){
        console.log(error_header);
        console.log('Unable to load resource (#' + resourceError.id + 'URL:' + resourceError.url + ')');
        console.log('Error code: ' + resourceError.errorCode + '. Description: ' + resourceError.errorString);
    }
};
// javascript in web page error
function onError(){
    // do nothing to avoid print error information to stdout.
}
// check if request is valid
function _valid_request(domain, root_domain){
    if (root_domain in _white_list){
        var domains = _white_list[root_domain];
        for (var i=0; i < domains.length; i++){
            if (domain.indexOf(domains[i]) != -1){
                return true;
            }
        }
        return false;
    } else {
        return false;
    }
}
// resource request callback, to cancel some request like css, etc.
function onResourceRequested(requestData, request){
    var domain = get_domain(requestData['url']);
    if ((/http:\/\/.+?\.css$/gi).test(requestData['url'])) {
        // abort all css request
        request.abort();
        return;
    } else if (root_domain != null && domain.indexOf(root_domain) == -1 && !_valid_request(domain, root_domain)){
        // abort request for other sites
        request.abort();
        return;
    }
}

if (args != undefined && args.length > 1){
    // set user apgent and referer
    args.forEach(function(arg, i){
        if (i == 0){
            // filename
            return;
        }
        if (i == 1){
            // first argument must be url
            url = arg;
            root_domain = get_root_domain(url);
            return;
        }
        if (arg.indexOf('=') == -1){
            // invalid arguments
            console.log('Invalid argument: ' + arg + ', arguments must be key=value');
            exit();
        }
        var pair = arg.split('=');
        if (pair.length != 2){
            console.log('Invalid argument: ' + arg + ', too many =');
            exit();
        }
        var key = pair[0];
        var value = pair[1];
        if (key == '--user-agent'){
            // set user agent
            user_agent = value;
        } else if (key == '--referer'){
            // set request referer
            referer = value;
        } else if (key == '--timeout'){
            // set request timeout
            timeout = parseInt(value);
        } else {
            console.log('Unknow argument: ' + arg);
            exit();
        }
    });
}

function download(url){
    // create page
    var page = require("webpage").create();

    // set callbacks
    page.onResourceTimeout = onResourceTimeout;
    page.onResourceError = onResourceError;
    page.onError = onError;
    page.onResourceRequested = onResourceRequested;

    // set timeout
    page.settings.resourceTimeout = timeout;
    page.settings.loadImages = false;
    if (user_agent != null){
        page.settings.userAgent = user_agent;
    }
    if (referer != null){
        page.customHeaders = {
            'Referer': referer
        };
    }
    // download page
    page.open(url, function(status){
        if (status !== 'success'){
            console.log(error_header);
            console.log('Status: ' + status);
        } else {
            console.log(page.content);
        }
        page.close();
        exit();
    });
}

if (url == null || url == undefined){
    console.log('Url not provided! You must provide url by --url=URL');
    exit();
} else {
    download(url);
}
