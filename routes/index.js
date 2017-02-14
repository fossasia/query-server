var express = require('express');
var router = express.Router();
var searcher = require('../server');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/search:query',function(req,res,next){
  // data = JSON.parse(req.body);
    data = req.params.query;
  console.log(data);
  console.log("Searching for: ",data);
  results = searcher(data);
  res.send(results);
});

module.exports = router;
