var gulp = require('gulp');
var sass = require('gulp-sass');
var useref = require('gulp-useref');
var del = require('del'); // delete the files
var runSequence = require('run-sequence');
var babel = require('gulp-babel');


gulp.task('sass', function(){
    return gulp.src('app/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('app/css'))

});

gulp.task('watch', function(){
    gulp.watch('app/scss/*.scss', ['sass']);
    gulp.watch('app/es6/*.js', ['babel']);
    gulp.watch('app/*.html', ['useref']);
});

gulp.task('useref', function(){
    return gulp.src('app/*.html')
        .pipe(useref())
        .pipe(gulp.dest('dist'))

});

gulp.task('fonts', function(){
    return gulp.src('app/fonts/**/*')
        .pipe(gulp.dest('dist/fonts'))
});

gulp.task('clean:dist', function(){
    return del.sync('dist');
});

gulp.task('babel', function(){
    return gulp.src('app/es6/*.js')
        .pipe(babel({
            presets: ['es2015']
        }))
        .pipe(gulp.dest('app/js'))
});

gulp.task('build', function(callback){
    runSequence('babel',
                ['fonts', 'sass', 'useref'],
                callback
            )
});
