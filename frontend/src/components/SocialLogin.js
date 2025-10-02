import React from 'react';

// Social logins (Google, Facebook, Apple) removed — keep a tiny placeholder
// component so the UI doesn't break. If you want the social buttons gone
// completely, remove the import and references in the parent components.
const SocialLogin = () => {
  return (
    <div className="text-sm text-gray-500">Social login disabled</div>
  );
};

export default SocialLogin;
