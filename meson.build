project('robotpy-rev', ['cpp'],
        default_options: ['warning_level=1', 'cpp_std=c++23',
                          'b_colorout=auto', 'optimization=2', 'b_pie=true'])

subdir('semiwrap')

rev_sources += files(
  'rev/rev.cpp',
)

# Match the vendor JSON: static REVLib/REVLibDriver, shared backend drivers.
# The shared libraries are supplied by the hatch-nativelib revlib dependency.
cpp = meson.get_compiler('cpp')
libs_path = meson.current_source_dir() + '/lib/lib'

rev_deps += [
    cpp.find_library('REVLibDriver', dirs: libs_path, static: true),
    cpp.find_library('REVLib', dirs: libs_path, static: true),
]

subdir('semiwrap/modules')
