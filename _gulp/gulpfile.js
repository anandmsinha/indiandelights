var gulp = require('gulp'),
    watch = require('gulp-watch'),
    prefix = require('gulp-autoprefixer'),
    sourcemaps = require('gulp-sourcemaps'),
    minifyCSS = require('gulp-minify-css'),
    less = require('gulp-less'),
    watch = require('gulp-watch'),
    gutil = require('gulp-util'),
    csso = require('gulp-csso'),
    coffee = require('gulp-coffee'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify')

gulp.task('newcss', function() {
    return gulp.src('less/new.less')
            .pipe(watch())
            .pipe(less())
            .pipe(prefix('Android 2.3',
                'Android >= 4',
                'Chrome >= 20',
                'Firefox >= 24',
                'Explorer >= 8',
                'iOS >= 6',
                'Opera >= 12',
                'Safari >= 6'
            ))
            .pipe(minifyCSS())
            .pipe(csso())
            .pipe(gulp.dest('../static/css/'));
})

gulp.task('javascript', function(){
    return gulp.src('coffee/app.coffee')
        .pipe(coffee({bare: true}))
        .on('error', gutil.log)
        .pipe(gulp.dest('../static/js'));
});

gulp.task('compilejavascript', ['javascript'], function() {
    return gulp.src(['bower_components/bootstrap/js/transition.js', 'bower_components/bootstrap/js/dropdown.js', 'bower_components/bootstrap/js/collapse.js', 'bower_components/bootstrap/js/carousel.js', '../static/js/toaster.min.js', '../static/js/app.js'])
            .pipe(concat('app.min.js'))
            .pipe(uglify())
            .on('error', gutil.log)
            .pipe(gulp.dest('../static/js'))
})

gulp.task('watcher', function() {
    gulp.watch('coffee/app.coffee', ['javascript', 'compilejavascript'])
})

gulp.task("default", function() {
    gulp.start('newcss', 'javascript', 'compilejavascript', 'watcher');
});