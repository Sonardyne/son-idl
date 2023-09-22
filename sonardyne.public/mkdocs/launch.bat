
START /B /WAIT cmd /c pip install mkdocs-material
START /B /WAIT cmd /c pip install mkdocs-glightbox
START /B /WAIT cmd /c pip install mkdocs-video
START /B /WAIT cmd /c pip install mkdocs-macros-plugin
START /B /WAIT cmd /c npm install
START /B /WAIT cmd /c npm update
START /B /WAIT cmd /c copy node_modules\@sonardyne\ui-markdown-assets\*.css .\docs\stylesheets\
START /B /WAIT cmd /c copy node_modules\@sonardyne\ui-markdown-assets\*.svg .\docs\assets\
