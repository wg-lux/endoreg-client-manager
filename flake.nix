{
  description = "Application packaged using poetry2nix";
  inputs = {
    # flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, tennis-data }:
    let
        system = "x86_64-linux";
        pkgs = nixpkgs.legacyPackages.${system};
        _poetry2nix = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };

    in
        {
          # Call with nix develop
          devShell."${system}" = pkgs.mkShell {
            buildInputs = [ 
              pkgs.poetry

              # Make venv (not very nixy but easy workaround to use current non-nix-packaged python module)
              pkgs.python3Packages.venvShellHook
            ];

            # Define Environment Variables
            DJANGO_SETTINGS_MODULE="endoreg_home.settings_dev";

            # Define Python venv
            venvDir = ".venv";
            postShellHook = ''
              mkdir -p data
              ln -snf ${tennis-data}/atp_matches_2020.csv data/dataset.csv

              pip install --upgrade pip
              poetry update

              export DJANGO_SECRET_KEY=$(cat .env/secret)

              # print out the environment variables
              echo "DJANGO_SECRET_KEY: $DJANGO_SECRET_KEY"

            '';
          };


        # });
        };
}
