// A simple bot that acts as admin user for the ninechan imageboard.
//
// Author: takeshix@adversec.com

// TODO Make it post comments and stuff

var zombie = require('zombie');
var assert  = require('assert');
var async = require('async');
var fs = require('fs');
var chance = require('chance');
var mongodb = require('mongodb');
var constants = require('./constants');

// Turn debug output on/off
var DEBUG = true;

// Target host, maybe get these from an external source
var host = '127.0.0.1';
var port = 5000;

// Images that should be uploaded by the admin user go here
var imageDir = 'ninechan-bot/static/images/';

zombie.localhost(host, port);
var browser = zombie.create();

function debug(msg){
  if(DEBUG){
    console.log('DEBUG: ' + msg);
  }
}

async.auto({
  get_credentials: function(callback){
    /*debug('Entering get_credentials function');
    mongodb.MongoClient.connect("mongodb://172.22.11.182:27017/ninechan-dev", function (error, db) {
      if (!error) {
        console.log("We are connected");
      }
      var users = db.collection('user');
      users.findOne({'username': 'admin'}, function (error, item) {
        callback(null, item['username'], item['password']);
      });
    });*/
    callback(null, 'admin', 'nimda123');
  },
  login: ['get_credentials', function(callback, credentials){
    debug('Entering login function');
    var username = credentials['get_credentials'][0];
    var password = credentials['get_credentials'][1];

    browser.visit('/login', function (error) {
      assert.ifError(error);

      browser.
          fill('username', username).
          fill('password', password).
          pressButton('doLogin', function(error){
            assert.ifError(error);
            browser.assert.success();
            console.log(browser.resources['0']['request']);
            console.log(browser.resources['0']['response']);
            callback(null);
          });
    });
  }],
  upload: ['login', function(callback){
    debug('Entering upload function');
    browser.visit('/post', function(error){
      assert.ifError(error);
      var availableImages = fs.readdirSync(imageDir);
      var image = availableImages[Math.floor(Math.random() * availableImages.length)];
      var randGen = chance();
      var description = randGen.paragraph();

      debug('Uploading image ' + image);

      browser.
        fill('title', constants.titles[Math.floor(Math.random() * constants.titles.length)]).
        fill('description', description).
        attach('image', imageDir + image).
        pressButton('doUpload', function(error) {
          assert.ifError(error);
          browser.assert.success();
          console.log(browser.resources['0']['request']);
          console.log(browser.resources['0']['response']);
          callback(null);
        });
    });
  }],
  logout: ['upload', function(callback){
      debug('Entering logout function');
      browser.visit('/logout', function(error){
        assert.ifError(error);
        console.log(browser.resources['0']['request']);
        console.log(browser.resources['0']['response']);
        callback(null);
      })
  }]
},
function(error, results){
  console.log('err = ', error);
  console.log('results = ', results);
});