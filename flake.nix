{
  description = "Application packaged using poetry2nix";
  inputs = {
    # flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    cachix = {
      url = "github:cachix/cachix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, cachix, ... }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.cudaSupport = true;
        };
        _poetry2nix = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        nvidiaCache = cachix.lib.mkCachixCache {
          inherit (pkgs) lib;
          name = "nvidia";
          publicKey = "nvidia.cachix.org-1:dSyZxI8geDCJrwgvBfPH3zHMC+PO6y/BT7O6zLBOv0w=";
          secretKey = null;  # not needed for pulling from the cache
        };

    in
        {
          # Call with nix develop
          devShell."${system}" = pkgs.mkShell {
            buildInputs = with pkgs; [ 
              poetry
              opencv
              tesseract

              # CUDA
              # cudatoolkit
              cudaPackages.cudnn
              cudaPackages.cudatoolkit 
              linuxPackages.nvidia_x11
              # cudaPackages.cudnn
              libGLU libGL
              glibc
              xorg.libXi xorg.libXmu freeglut
              xorg.libXext xorg.libX11 xorg.libXv xorg.libXrandr zlib 
              ncurses5 stdenv.cc binutils

              python311
              python311Packages.pandas
              python311Packages.pytesseract
              python311Packages.venvShellHook
              python311Packages.numpy
              python311Packages.torchvision-bin
              python311Packages.torchaudio-bin

              pam

            ];

            # Define Environment Variables
            DJANGO_SETTINGS_MODULE="endoreg_client_manager.settings";

            # Define Python venv
            venvDir = ".venv";
            postShellHook = ''
              export CUDA_PATH=${pkgs.cudatoolkit}
              # export LD_LIBRARY_PATH=${pkgs.linuxPackages.nvidia_x11}/lib:${pkgs.ncurses5}/lib
              # LD_LIBRARY_PATH = "${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib";
              export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
              export EXTRA_CCFLAGS="-I/usr/include"
              mkdir -p data

              python -m pip install --upgrade pip
              poetry update

              # install dev dependiencies
              # python -m pip install -e /home/agl-admin/dev/agl-frame-extractor
              # python -m pip install -e /home/agl-admin/dev/endoreg-db
              # pip install -e /home/agl-admin/dev/agl-predict-endo-frame
              
              export DJANGO_SECRET_KEY=$(cat .env/secret)
            '';
          };

        nixConfig = {
          binary-caches = [nvidiaCache.binaryCachePublicUrl];
          binary-cache-public-keys = [nvidiaCache.publicKey];
        };
      };
}
