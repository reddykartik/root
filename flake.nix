{
  description = "environment setup";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/84e56bf5e919f86ab5309ebc00edd188752aad25";
  outputs = { self, nixpkgs }:
  let system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (python314.withPackages (ps: with ps; [
          numpy
          pandas
          scikit-learn
          matplotlib
          seaborn
          notebook
        ]))
      ];
    };
  };
}
