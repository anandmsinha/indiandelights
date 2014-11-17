/**
 * Created by A007ms on 9/7/14.
 */
var gulp = require('gulp'),
    watch = require('gulp-watch'),
    prefix = require('gulp-autoprefixer'),
    sourcemaps = require('gulp-sourcemaps'),
    minifyCSS = require('gulp-minify-css'),
    less = require('gulp-less'),
    watch = require('gulp-watch'),
    gutil = require('gulp-util'),
    csso = require('gulp-csso'),
    coffee = require('gulp-coffee');

gulp.task('movefiles', function() {
    /*return gulp.src('bower_components/bootstrap/dist/**').
        pipe(gulp.dest('../static/'));*/
});

gulp.task('newcss', function() {
    return gulp.src('less/new.less')
            .pipe(watch())
            .pipe(less())
            .pipe(prefix('Android 2.3',
                'Android >= 4',
                'Chrome >= 20',
                'Firefox >= 24', // Firefox 24 is the latest ESR
                'Explorer >= 8',
                'iOS >= 6',
                'Opera >= 12',
                'Safari >= 6'
            ))
            .pipe(minifyCSS())
            .pipe(csso())
            .pipe(gulp.dest('../static/css/'));
})

gulp.task('css', function() {
    return gulp.src('less/custom.less').
        pipe(watch()).
        pipe(less()).
        pipe(prefix('Android 2.3',
            'Android >= 4',
            'Chrome >= 20',
            'Firefox >= 24', // Firefox 24 is the latest ESR
            'Explorer >= 8',
            'iOS >= 6',
            'Opera >= 12',
            'Safari >= 6'
        )).
        pipe(minifyCSS()).
        pipe(csso()).
        on('error', gutil.log).
        pipe(gulp.dest('../static/css/'));
});

gulp.task('javascript', function(){
    return gulp.src('coffee/app.coffee').
        pipe(watch()).
        pipe(coffee({bare: true})).
        on('error', gutil.log).
        pipe(gulp.dest('../static/js'));
});

gulp.task("default", function() {
    gulp.start('newcss', 'css', 'javascript');
});