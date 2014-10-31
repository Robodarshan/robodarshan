module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),    
    shell: {
        restartGunicorn: {
            command: 'kill -HUP `cat gunicorn.pid`'
        }
    },
    watch: {
      options: {
	livereload: true,
      },
      template: {
        files: ['**/*.html', '**/*.css', '**/*.js'],
      },
      python: {
        files: ['**/*.py',],
        tasks: ['shell',],
      }
    },
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');
  // Default task(s).
  grunt.registerTask('default', ['shell', 'watch']);

};