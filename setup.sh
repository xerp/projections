#!/bin/sh

SRC_DIR=bin/
DEST_DIR_NAME=projections
DEST_DIR=/usr/lib/$DEST_DIR_NAME
BIN_FILE=/usr/bin/projections
DESKTOP_ENTRY=projections.desktop
DESKTOP_ENTRY_DIR=/usr/share/applications

install(){

  if [ ! -d "$DEST_DIR" ]
  then
    mkdir -p $DEST_DIR
  fi

  echo "Installing app on $DEST_DIR"
  cp -R $SRC_DIR/* $DEST_DIR

  echo 'Deploying app on bin dir'
  echo "#!/bin/sh\npython $DEST_DIR/projections.py" > $DEST_DIR/projections
  chmod 755 $DEST_DIR/projections
  ln -s $DEST_DIR/projections $BIN_FILE 2> /dev/null

  echo 'Creating a desktop entry'
  cp $DESKTOP_ENTRY $DESKTOP_ENTRY_DIR/
  chmod 644 $DESKTOP_ENTRY_DIR/$DESKTOP_ENTRY

}

uninstall(){
  echo "Uninstall app"
  rm -R $DEST_DIR

  rm $BIN_FILE
  rm $DESKTOP_ENTRY_DIR/$DESKTOP_ENTRY

}

if [ `id -u` != 0 ]
then
  echo 'You are not root'
  exit
fi

if [ "$1" = "install" ]
then
  install
else
  uninstall
fi
