@echo off

:: Define variables
set CONTAINER_NAME=lockduck
set TAG=0.1
set IMAGE_NAME=lockduck-img:%TAG%
set VOLUME_NAME=lockduck_db
set VOLUME_MOUNT_PATH=/mnt

:: Check if the image already exists
docker images --format "{{.Repository}}:{{.Tag}}" | findstr "%IMAGE_NAME%" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Image %IMAGE_NAME% not found. Building the image...
    docker build -t %IMAGE_NAME% . || (
        echo Failed to build the image.
        exit /b 1
    )
) else (
    echo Image %IMAGE_NAME% already exists. Skipping build.
)

:: Check if volume exists
for /f "tokens=*" %%V in ('docker volume ls --filter "name=%VOLUME_NAME%" -q') do set VOLUME_EXISTS=%%V

:: Create the volume if it doesn't exist
if not defined VOLUME_EXISTS (
    echo Volume %VOLUME_NAME% does not exist. Creating it...
    docker volume create %VOLUME_NAME%
) else (
    echo Volume %VOLUME_NAME% already exists. Skipping creation.
)

:: Run the container
for /f "tokens=*" %%C in ('docker ps -a --filter "name=%CONTAINER_NAME%" -q') do set CONTAINER_EXISTS=%%C

cls
if not defined CONTAINER_EXISTS (
    docker run -it -v %VOLUME_NAME%:%VOLUME_MOUNT_PATH% --name %CONTAINER_NAME% %IMAGE_NAME%
) else (
    docker container start -i %CONTAINER_NAME%
)
